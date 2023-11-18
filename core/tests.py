from django.test import TestCase, Client
from django.contrib.auth.models import User


class AuthTokenTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")

    def test_auth_token_success(self):
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

    def test_auth_token_failure(self):
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
