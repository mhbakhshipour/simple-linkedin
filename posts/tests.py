from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from relationships.models import Follow
from .models import Post


class FeedTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="user@example.com", password="pass1234")
        self.other = User.objects.create_user(email="other@example.com", password="pass1234")

    def test_root_redirects_to_feed(self):
        self.client.login(email="user@example.com", password="pass1234")
        response = self.client.get("/", follow=True)
        self.assertRedirects(response, reverse("posts:feed"))

    def test_feed_requires_login(self):
        response = self.client.get(reverse("posts:feed"))
        self.assertEqual(response.status_code, 302)

    def test_post_creation_from_feed(self):
        self.client.login(email="user@example.com", password="pass1234")
        response = self.client.post(
            reverse("posts:feed"),
            {"body": "Hello world"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Post.objects.filter(author=self.user, body="Hello world").exists())

    def test_feed_shows_only_self_and_following_posts(self):
        self.client.login(email="user@example.com", password="pass1234")
        other2 = User.objects.create_user(email="third@example.com", password="pass1234")
        post_self = Post.objects.create(author=self.user, body="from self")
        post_followed = Post.objects.create(author=self.other, body="from followed")
        post_unfollowed = Post.objects.create(author=other2, body="from unfollowed")
        Follow.objects.create(follower=self.user, following=self.other)
        response = self.client.get(reverse("posts:feed"))
        self.assertContains(response, post_self.body)
        self.assertContains(response, post_followed.body)
        self.assertNotContains(response, post_unfollowed.body)

    def test_user_can_edit_own_post(self):
        self.client.login(email="user@example.com", password="pass1234")
        post = Post.objects.create(author=self.user, body="original")
        response = self.client.post(
            reverse("posts:edit", args=[post.pk]),
            {"body": "updated"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        post.refresh_from_db()
        self.assertEqual(post.body, "updated")

    def test_user_can_delete_own_post(self):
        self.client.login(email="user@example.com", password="pass1234")
        post = Post.objects.create(author=self.user, body="to delete")
        response = self.client.post(
            reverse("posts:delete", args=[post.pk]),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Post.objects.filter(pk=post.pk).exists())
