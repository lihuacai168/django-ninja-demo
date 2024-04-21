from django.test import TestCase, Client
from django.contrib.auth.models import User

from core.service import GenericCURD


class AuthTokenTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")

    def test_get_token_fresh_success(self):
        """Test obtain pair token
        """
        response = self.client.post(
            "/api/token/pair",
            {"username": "testuser", "password": "12345"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        response_data = response.json()

        self.assertIn("access", response_data["data"])
        self.assertIn("refresh", response_data["data"])

        user_data = response_data["data"]["user"]
        self.assertEqual(user_data["email"], self.user.email)
        self.assertEqual(user_data["first_name"], self.user.first_name)

        self.assertEqual(response_data["success"], True)

        response = self.client.post(
            "/api/token/refresh",
            data={"refresh": response_data["data"]["refresh"]},
            content_type="application/json",
        ).json()
        self.assertEqual(response['data']['refresh'], response_data['data']['refresh'])

    def test_auth_token_failure_wrong_user_and_password(self):
        """Test the failure of authentication token generation.
        """
        response = self.client.post(
            "/api/token/pair",
            {"username": "wronguser", "password": "wrongpassword"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["success"], False)
        self.assertIn("message", response.json())
        self.assertIn(
            "No active account found with the given credentials",
            response.json()["message"],
        )

    def test_auth_token_failure_right_user_and_wrong_password(self):
        """Test the failure of authentication token generation.
        """
        response = self.client.post(
            "/api/token/pair",
            {"username": "testuser", "password": "wrongpassword"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["success"], False)
        self.assertIn("message", response.json())
        self.assertIn(
            "No active account found with the given credentials",
            response.json()["message"],
        )

    def test_refresh_token_failure(self):
        response = self.client.post(
            "/api/token/refresh",
            data={"refresh": "12345"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 401)

    def test_access_token_failure(self):
        response = self.client.post(
            "/api/token/refresh",
            data={"refresh": "12345"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 401)