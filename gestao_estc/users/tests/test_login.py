from django.urls import reverse
from rest_framework import status
from .default_test_case import DefaultTestCase
from ..models import User


class LoginViewTest(DefaultTestCase):
    @classmethod
    def message_test(cls):
        print("=" * 50)
        print("LoginView tests")
        print("=" * 50)

    def setUp(self):
        self.url_login = reverse("user-login")
        self.valid_login_data = {"username": "JUorlando", "password": "senha123"}
        self.invalid_login_data = {"username": "JUorlando", "password": "wrongpassword"}

    def test_login_success(self):

        User.objects.create_user(
            username="JUorlando", email="juorlando@example.com", password="senha123"
        )

        response = self.client.post(
            self.url_login,
            {"username": "JUorlando", "password": "senha123"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_invalid_credentials(self):
        response = self.client.post(
            self.url_login, self.invalid_login_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)
        self.assertEqual(
            response.data["detail"], "Não existe uma conta com esses dados."
        )
        print("test_login_invalid_credentials - OK")

    def test_login_missing_fields(self):
        response = self.client.post(self.url_login, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)
        self.assertIn("password", response.data)
