# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('entrada/', views.registrar_entrada, name='registrar_entrada'),
    path('saida/', views.registrar_saida, name='registrar_saida'),
    path('valor/', views.calcular_valor, name='calcular_valor'),
    path('pagar/', views.registrar_pagamento, name='registrar_pagamento'),
]

