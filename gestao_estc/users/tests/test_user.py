from django.urls import reverse
from rest_framework import status
from .default_test_case import DefaultTestCase


class UserViewTest(DefaultTestCase):
    @classmethod
    def message_test(cls):
        print("=" * 50)
        print("UserView tests")
        print("=" * 50)

    def setUp(self):
        self.url_list_create_user = reverse("user-create")
        self.valid_user_data = {
            "username": "JUorlando",
            "email": "juorlando@example.com",
            "password": "senha123",
            "first_name": "Junior Orlando",
            "last_name": "",
        }

    def test_create_user_success(self):
        response = self.client.post(
            self.url_list_create_user, self.valid_user_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertEqual(response.data["username"], self.valid_user_data["username"])
        print("test_create_user_success - OK")

    def test_create_user_invalid_data(self):
        invalid_data = {
            "username": "JUorlando",
            "email": "invalid-email",
            "password": "senha123",
            "first_name": "",
            "last_name": "",
        }
        response = self.client.post(
            self.url_list_create_user, invalid_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertIn("first_name", response.data)
        print("test_create_user_invalid_data - OK")

    def test_list_user_by_id_success(self):
        create_response = self.client.post(
            self.url_list_create_user, self.valid_user_data, format="json"
        )
        user_id = create_response.data["id"]
        url_retrieve_user = reverse("user-detail", kwargs={"pk": user_id})
        response = self.client.get(url_retrieve_user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], user_id)
        self.assertEqual(response.data["username"], self.valid_user_data["username"])
        print("test_list_user_by_id_success - OK")
