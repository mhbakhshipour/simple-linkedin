from django.test import TestCase
from django.urls import reverse

from .models import User


class UserManagerTests(TestCase):
    def test_create_user_with_email(self):
        user = User.objects.create_user(email="test@example.com", password="pass1234")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("pass1234"))

    def test_create_superuser_flags(self):
        user = User.objects.create_superuser(email="admin@example.com", password="admin1234")
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


class AuthViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="user@example.com", password="pass1234")

    def test_signup_creates_user_and_logs_in(self):
        response = self.client.post(
            reverse("accounts:signup"),
            {
                "email": "new@example.com",
                "first_name": "New",
                "last_name": "User",
                "password1": "pass1234",
                "password2": "pass1234",
            },
            follow=True,
        )
        self.assertRedirects(response, reverse("posts:feed"))
        self.assertTrue(User.objects.filter(email="new@example.com").exists())
        self.assertTrue(response.context["user"].is_authenticated)

    def test_login_with_valid_credentials(self):
        response = self.client.post(
            reverse("accounts:login"),
            {"email": "user@example.com", "password": "pass1234"},
            follow=True,
        )
        self.assertRedirects(response, reverse("posts:feed"))
        self.assertTrue(response.context["user"].is_authenticated)

    def test_login_with_invalid_credentials_shows_form(self):
        response = self.client.post(
            reverse("accounts:login"),
            {"email": "user@example.com", "password": "wrong"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid email or password", status_code=200)

    def test_logout_logs_user_out(self):
        self.client.login(email="user@example.com", password="pass1234")
        response = self.client.post(reverse("accounts:logout"), follow=True)
        self.assertRedirects(response, reverse("accounts:login"))
        self.assertFalse(response.context["user"].is_authenticated)
