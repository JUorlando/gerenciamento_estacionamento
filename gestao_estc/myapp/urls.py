# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("entrada/", views.RegistrarEntradaView.as_view(), name="entrada"),
    path("saida/", views.RegistrarSaidaView.as_view(), name="saida"),
    path("valor/", views.CalcularValorView.as_view(), name="valor"),
    path("pagar/", views.RegistrarPagamentoView.as_view(), name="pagar"),
    path("relatorio/", views.RelatorioView.as_view(), name="relatorio"),
]
