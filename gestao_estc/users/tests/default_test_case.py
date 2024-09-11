from django.test import TestCase
from rest_framework.test import APIClient
from ..models import User
from rest_framework import status
from rest_framework.utils.serializer_helpers import ReturnList


class DefaultTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        ...

    @classmethod
    def setUpClass(cls):
        cls.user_request = {
            "username": "JUolando",
            "email": "juorlando@example.com",
            "password": "senha123",
            "first_name": "Junior Orlando",
            "last_name": "",
        }

        cls.user_login = {"username": "JUorlando", "password": "senha123"}

        cls.url_login = "/api/login/"
        cls.url_requests = "/api/users/"
        cls.url_retrieve_user_not_found = "/api/users/99999/"

        cls.message_test()

    @classmethod
    def tearDownClass(cls):
        print("=" * 50)

    @classmethod
    def setUp(cls):
        cls.user = User.objects.create_user(**cls.user_request)

        cls.url_retrieve_user = f"/api/users/{cls.user.id}/"

    @classmethod
    def message_test(cls):
        print("=" * 50)

    @classmethod
    def login_apiclient(cls, login_data, auth=True):
        client_login = APIClient()

        if not auth:
            return client_login

        login_response = client_login.post(cls.url_login, login_data, format="json")
        token = login_response.data["access"]

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

        return client

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
