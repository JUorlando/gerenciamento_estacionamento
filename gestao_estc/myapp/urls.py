from django.urls import path
from .views import registrar_entrada

urlpatterns = [
    path('entrada', registrar_entrada),
]
