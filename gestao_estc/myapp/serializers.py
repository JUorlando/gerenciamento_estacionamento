from rest_framework import serializers
from .models import EntradaDeVeiculo

class EntradaDeVeiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntradaDeVeiculo
        fields = ['placa', 'data_entrada']
