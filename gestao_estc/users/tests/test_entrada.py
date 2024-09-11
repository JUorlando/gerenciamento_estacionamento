from django.urls import reverse
from rest_framework import status
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

class RegistrarEntradaViewTest(DefaultTestCase):
    @classmethod
    def message_test(cls):
        print("=" * 50)
        print("RegistrarEntradaView tests")
        print("=" * 50)

    def setUp(self):
        super().setUp()
        self.url_registrar_entrada = reverse("entrada")
        self.valid_entrada_data = {"placa": "ABC1234"}

    def test_registrar_entrada_success(self):
        response = self.client.post(self.url_registrar_entrada, self.valid_entrada_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("placa", response.data)
        self.assertEqual(response.data["placa"], self.valid_entrada_data["placa"])
        print("test_registrar_entrada_success - OK")

    def test_registrar_entrada_missing_placa(self):
        response = self.client.post(self.url_registrar_entrada, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Placa é obrigatória")
        print("test_registrar_entrada_missing_placa - OK")

