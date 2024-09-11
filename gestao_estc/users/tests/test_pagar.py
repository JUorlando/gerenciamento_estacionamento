from django.urls import reverse
from rest_framework import status
from .default_test_case import DefaultTestCase
from myapp.models import EntradaDeVeiculo, SaidaDeVeiculo
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

class DefaultTestCase(APITestCase):
    def setUp(self):
        super().setUp()

        self.user = get_user_model().objects.create_user(
            username='JUorlando',
            password='senha123',
            email='juorlando@example.com'
        )
        self.token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def get_jwt_token(self, user):
        """
        Obtém o token JWT para um usuário.
        """
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class RegistrarPagamentoViewTest(DefaultTestCase):
    @classmethod
    def message_test(cls):
        print("=" * 50)
        print("RegistrarPagamentoView tests")
        print("=" * 50)

    def setUp(self):
        super().setUp()
        self.url_registrar_pagamento = reverse("pagar")
        self.placa = "LMN9012"
        self.entrada = EntradaDeVeiculo.objects.create(placa=self.placa)

    def test_registrar_pagamento_success(self):
        response = self.client.post(self.url_registrar_pagamento, {"placa": self.placa}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("valor_pago", response.data)
        self.assertTrue(SaidaDeVeiculo.objects.filter(entrada=self.entrada).exists())
        print("test_registrar_pagamento_success - OK")

    def test_registrar_pagamento_veiculo_nao_registrado(self):
        response = self.client.post(self.url_registrar_pagamento, {"placa": "NOT_FOUND"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Veículo não registrado")
        print("test_registrar_pagamento_veiculo_nao_registrado - OK")
