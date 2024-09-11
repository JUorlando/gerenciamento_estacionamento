from django.urls import reverse
from rest_framework import status
from .default_test_case import DefaultTestCase
from myapp.models import EntradaDeVeiculo, SaidaDeVeiculo
from django.utils import timezone
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken


class DefaultTestCase(APITestCase):
    def setUp(self):
        super().setUp()

        self.user = get_user_model().objects.create_user(
            username="JUorlando", password="senha123", email="juorlando@example.com"
        )
        self.token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def get_jwt_token(self, user):
        """
        Obtém o token JWT para um usuário.
        """
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class RegistrarSaidaViewTest(DefaultTestCase):
    @classmethod
    def message_test(cls):
        print("=" * 50)
        print("RegistrarSaidaView tests")
        print("=" * 50)

    def setUp(self):
        super().setUp()
        self.url_registrar_saida = reverse("saida")
        self.placa = "OPQ3456"
        self.entrada = EntradaDeVeiculo.objects.create(placa=self.placa)
        self.saida = SaidaDeVeiculo.objects.create(entrada=self.entrada, pago=True)

    def test_registrar_saida_success(self):
        response = self.client.post(
            self.url_registrar_saida, {"placa": self.placa}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["placa"], self.placa)
        print("test_registrar_saida_success - OK")

    def test_registrar_saida_veiculo_nao_registrado(self):
        response = self.client.post(
            self.url_registrar_saida, {"placa": "NOT_FOUND"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Veículo não registrado")
        print("test_registrar_saida_veiculo_nao_registrado - OK")

    def test_registrar_saida_pagamento_nao_realizado(self):
        entrada_sem_pagamento = EntradaDeVeiculo.objects.create(placa="NEW_PLATE")
        response = self.client.post(
            self.url_registrar_saida,
            {"placa": entrada_sem_pagamento.placa},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(
            response.data["error"], "O pagamento deve ser realizado antes da saída"
        )
        print("test_registrar_saida_pagamento_nao_realizado - OK")
