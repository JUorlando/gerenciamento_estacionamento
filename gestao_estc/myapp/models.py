from django.db import models

class EntradaDeVeiculo(models.Model):
    placa = models.CharField(max_length=7)
    data_entrada = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.placa

