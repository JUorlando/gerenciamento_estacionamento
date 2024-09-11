from django.urls import reverse
from rest_framework import status
from .default_test_case import DefaultTestCase
from myapp.models import EntradaDeVeiculo
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

class CalcularValorViewTest(DefaultTestCase):
    @classmethod
    def message_test(cls):
        print("=" * 50)
        print("CalcularValorView tests")
        print("=" * 50)

    def setUp(self):
        super().setUp()
        self.url_calcular_valor = reverse("valor")
        self.placa = "XYZ5678"
        EntradaDeVeiculo.objects.create(placa=self.placa)

    def test_calcular_valor_success(self):
        response = self.client.get(self.url_calcular_valor, {"placa": self.placa}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("valor_a_pagar", response.data)
        print("test_calcular_valor_success - OK")

    def test_calcular_valor_missing_placa(self):
        response = self.client.get(self.url_calcular_valor, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Placa é obrigatória")
        print("test_calcular_valor_missing_placa - OK")

    def test_calcular_valor_veiculo_nao_registrado(self):
        response = self.client.get(self.url_calcular_valor, {"placa": "NOT_FOUND"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Veículo não registrado")
        print("test_calcular_valor_veiculo_nao_registrado - OK")
