# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('entrada/', views.RegistrarEntradaView.as_view()),
    path('saida/', views.RegistrarSaidaView.as_view()),
    path('valor/', views.CalcularValorView.as_view()),
    path('pagar/', views.RegistrarPagamentoView.as_view()),
    path('relatorio/', views.RelatorioView.as_view()),
]

