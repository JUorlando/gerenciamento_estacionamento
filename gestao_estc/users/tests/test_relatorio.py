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


class RelatorioViewTest(DefaultTestCase):
    @classmethod
    def message_test(cls):
        print("=" * 50)
        print("RelatorioView tests")
        print("=" * 50)

    def setUp(self):
        super().setUp()
        self.url_relatorio = reverse("relatorio")
        self.entrada = EntradaDeVeiculo.objects.create(placa="RST6789")
        self.saida = SaidaDeVeiculo.objects.create(entrada=self.entrada, pago=True)


    def test_relatorio_success(self):
        response = self.client.get(self.url_relatorio)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreater(len(response.data), 0)
        print("test_relatorio_success - OK")


    def test_relatorio_sem_entradas(self):
        EntradaDeVeiculo.objects.all().delete()
        response = self.client.get(self.url_relatorio)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 0)
        print("test_relatorio_sem_entradas - OK")
