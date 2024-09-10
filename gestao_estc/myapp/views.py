from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import EntradaDeVeiculo, SaidaDeVeiculo
from django.utils import timezone
import os

ESTACIONAMENTO_VALOR_HORA = float(os.getenv("ESTACIONAMENTO_VALOR_HORA", 5.00))
TOLERANCIA_TEMPO_SAIDA = int(os.getenv("TOLERANCIA_TEMPO_SAIDA", 15))


@api_view(["POST"])
def registrar_entrada(request):
    placa = request.data.get("placa")
    if not placa:
        return Response(
            {"error": "Placa é obrigatória"}, status=status.HTTP_400_BAD_REQUEST
        )

    entrada = EntradaDeVeiculo.objects.create(placa=placa)
    return Response(
        {"placa": entrada.placa, "data_entrada": entrada.data_entrada},
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
def registrar_saida(request):
    placa = request.data.get("placa")
    pago = request.data.get("pago", False)

    entrada = get_object_or_404(EntradaDeVeiculo, placa=placa)

    if not pago:
        return Response(
            {"error": "O pagamento deve ser realizado antes da saída"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    delta = timezone.now() - entrada.data_entrada
    minutos = delta.total_seconds() / 60

    if minutos > TOLERANCIA_TEMPO_SAIDA:
        return Response(
            {"error": "Tempo de tolerância excedido"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    saida = SaidaDeVeiculo.objects.create(entrada=entrada, pago=pago)
    return Response(
        {"placa": saida.entrada.placa, "data_saida": saida.data_saida},
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET"])
def calcular_valor(request):
    placa = request.query_params.get("placa")
    if not placa:
        return Response(
            {"error": "Placa é obrigatória"}, status=status.HTTP_400_BAD_REQUEST
        )

    entrada = get_object_or_404(EntradaDeVeiculo, placa=placa)
    delta = timezone.now() - entrada.data_entrada
    horas = delta.total_seconds() / 3600
    valor = ESTACIONAMENTO_VALOR_HORA * (
        int(horas) + 1
    )

    return Response({"placa": placa, "valor_a_pagar": valor}, status=status.HTTP_200_OK)


@api_view(["POST"])
def registrar_pagamento(request):
    placa = request.data.get("placa")

    entrada = get_object_or_404(EntradaDeVeiculo, placa=placa)
    valor = ESTACIONAMENTO_VALOR_HORA * (
        int((timezone.now() - entrada.data_entrada).total_seconds() / 3600) + 1
    )

    saida, created = SaidaDeVeiculo.objects.get_or_create(entrada=entrada)
    saida.pago = True
    saida.valor_pago = valor
    saida.save()

    return Response(
        {"message": "Pagamento realizado com sucesso", "valor_pago": saida.valor_pago},
        status=status.HTTP_200_OK,
    )
