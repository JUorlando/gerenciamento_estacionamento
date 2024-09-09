from django.db import models
from django.utils import timezone

class EntradaDeVeiculo(models.Model):
    placa = models.CharField(max_length=7)
    data_entrada = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.placa

class SaidaDeVeiculo(models.Model):
    entrada = models.OneToOneField(EntradaDeVeiculo, on_delete=models.CASCADE)
    data_saida = models.DateTimeField(default=timezone.now)
    pago = models.BooleanField(default=False)
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.entrada.placa