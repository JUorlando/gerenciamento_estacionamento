from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import EntradaDeVeiculo, SaidaDeVeiculo
from django.utils import timezone
import os

ESTACIONAMENTO_VALOR_HORA = float(os.getenv("ESTACIONAMENTO_VALOR_HORA", 5.00))
TOLERANCIA_TEMPO_SAIDA = int(os.getenv("TOLERANCIA_TEMPO_SAIDA", 15))


def calcular_valor(entrada):
    delta = timezone.now() - entrada.data_entrada
    horas = delta.total_seconds() / 3600
    valor = ESTACIONAMENTO_VALOR_HORA * (int(horas) + 1)
    return valor


class RegistrarEntradaView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
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


class CalcularValorView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        placa = request.query_params.get("placa")
        if not placa:
            return Response(
                {"error": "Placa é obrigatória"}, status=status.HTTP_400_BAD_REQUEST
            )

        entrada = (
            EntradaDeVeiculo.objects.filter(placa=placa)
            .order_by("-data_entrada")
            .first()
        )
        if not entrada:
            return Response(
                {"error": "Veículo não registrado"}, status=status.HTTP_404_NOT_FOUND
            )

        valor = calcular_valor(entrada)

        return Response(
            {"placa": placa, "valor_a_pagar": valor}, status=status.HTTP_200_OK
        )


class RegistrarPagamentoView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        placa = request.data.get("placa")

        entrada = (
            EntradaDeVeiculo.objects.filter(placa=placa)
            .order_by("-data_entrada")
            .first()
        )
        if not entrada:
            return Response(
                {"error": "Veículo não registrado"}, status=status.HTTP_404_NOT_FOUND
            )

        valor = calcular_valor(entrada)

        saida, created = SaidaDeVeiculo.objects.get_or_create(entrada=entrada)
        saida.pago = True
        saida.valor_pago = valor
        saida.save()

        return Response(
            {
                "message": "Pagamento realizado com sucesso",
                "valor_pago": saida.valor_pago,
            },
            status=status.HTTP_200_OK,
        )


class RegistrarSaidaView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        placa = request.data.get("placa")
        if not placa:
            return Response(
                {"error": "Placa é obrigatória"}, status=status.HTTP_400_BAD_REQUEST
            )

        entrada = (
            EntradaDeVeiculo.objects.filter(placa=placa)
            .order_by("-data_entrada")
            .first()
        )
        if not entrada:
            return Response(
                {"error": "Veículo não registrado"}, status=status.HTTP_404_NOT_FOUND
            )

        saida = SaidaDeVeiculo.objects.filter(entrada=entrada).first()
        if not saida or not saida.pago:
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

        saida.data_saida = timezone.now()
        saida.save()

        return Response(
            {"placa": saida.entrada.placa, "data_saida": saida.data_saida},
            status=status.HTTP_201_CREATED,
        )
