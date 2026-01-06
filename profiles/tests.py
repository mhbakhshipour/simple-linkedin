from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from .models import Profile


class ProfileTests(TestCase):
    def test_profile_created_for_new_user(self):
        user = User.objects.create_user(email="test@example.com", password="pass1234")
        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_profile_detail_view(self):
        user = User.objects.create_user(email="test@example.com", password="pass1234")
        response = self.client.get(reverse("profiles:detail", args=[user.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertIn("profile", response.context)

    def test_profile_edit_requires_login(self):
        response = self.client.get(reverse("profiles:edit"))
        self.assertEqual(response.status_code, 302)

    def test_profile_edit_updates_headline(self):
        user = User.objects.create_user(email="test@example.com", password="pass1234")
        self.client.login(email="test@example.com", password="pass1234")
        response = self.client.post(
            reverse("profiles:edit"),
            {"headline": "New headline", "bio": ""},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        user.refresh_from_db()
        self.assertEqual(user.profile.headline, "New headline")

    def test_search_finds_user_by_name(self):
        user = User.objects.create_user(
            email="jane@example.com",
            password="pass1234",
            first_name="Jane",
            last_name="Doe",
        )
        response = self.client.get(reverse("profiles:search"), {"q": "Jane"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Jane Doe")
