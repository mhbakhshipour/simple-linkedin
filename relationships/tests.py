from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from .models import Follow


class FollowViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="user@example.com", password="pass1234")
        self.other = User.objects.create_user(email="other@example.com", password="pass1234")

    def test_follow_creates_relationship(self):
        self.client.login(email="user@example.com", password="pass1234")
        response = self.client.post(reverse("relationships:follow", args=[self.other.pk]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Follow.objects.filter(follower=self.user, following=self.other).exists())

    def test_unfollow_removes_relationship(self):
        Follow.objects.create(follower=self.user, following=self.other)
        self.client.login(email="user@example.com", password="pass1234")
        response = self.client.post(reverse("relationships:unfollow", args=[self.other.pk]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Follow.objects.filter(follower=self.user, following=self.other).exists())

    def test_cannot_follow_self(self):
        self.client.login(email="user@example.com", password="pass1234")
        self.client.post(reverse("relationships:follow", args=[self.user.pk]))
        self.assertFalse(Follow.objects.filter(follower=self.user, following=self.user).exists())
