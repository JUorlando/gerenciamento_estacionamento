from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.utils.serializer_helpers import ReturnList
from django.urls import reverse
from ..models import User

class DefaultTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_request = {
            "username": "JUorlando",
            "email": "juorlando@example.com",
            "password": "senha123",
            "first_name": "Junior Orlando",
            "last_name": "",
        }

        cls.user_login = {"username": "JUorlando", "password": "senha123"}

        cls.url_login = "/api/users/login/"
        cls.url_requests = "/api/users/"
        cls.url_retrieve_user_not_found = "/api/users/99999/"

        cls.message_test()

    @classmethod
    def tearDownClass(cls):
        print("=" * 50)

    @classmethod
    def setUp(cls):
        cls.client = APIClient()  # Inicializa o cliente da API
        cls.user = User.objects.create_user(**cls.user_request)
        cls.url_retrieve_user = f"/api/users/{cls.user.id}/"
        cls.client = cls.login_apiclient(cls.user_login)

    @classmethod
    def message_test(cls):
        print("=" * 50)

    @classmethod
    def login_apiclient(cls, user_login):
        login_url = reverse("user-login")
        response = cls.client.post(login_url, user_login, format="json")

        if response.status_code == 200:
            token = response.data.get("access")
            if not token:
                raise ValueError("A chave 'access' não foi encontrada na resposta.")
            cls.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
            return cls.client
        else:
            raise ValueError("Falha ao fazer login.")

    def responseAssertMissingToken(self, response):
        """Response detail: Authentication credentials were not provided."""
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertIn("detail", response.data)
        self.assertEqual(
            str(response.data["detail"]),
            "Authentication credentials were not provided.",
        )

    def responseAssertNotFound(self, response):
        """Response detail: not found."""
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertIn("detail", response.data)
        self.assertEqual("Not found.", str(response.data["detail"]))

    def responseAssertPaginatedList(self, response):
        """Response paginated list"""
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIn("count", response.data)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)
        self.assertIn("results", response.data)
        self.assertIsInstance(response.data["results"], ReturnList)

