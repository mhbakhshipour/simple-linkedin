from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from .models import Conversation, Message


class MessagingViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="user@example.com", password="pass1234")
        self.other = User.objects.create_user(email="other@example.com", password="pass1234")

    def test_inbox_requires_login(self):
        response = self.client.get(reverse("messaging:inbox"))
        self.assertEqual(response.status_code, 302)

    def test_start_conversation_creates_conversation(self):
        self.client.login(email="user@example.com", password="pass1234")
        response = self.client.get(reverse("messaging:start", args=[self.other.pk]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Conversation.objects.count(), 1)

    def test_conversation_detail_sends_message(self):
        conversation = Conversation.objects.create(user1=self.user, user2=self.other)
        self.client.login(email="user@example.com", password="pass1234")
        response = self.client.post(
            reverse("messaging:conversation", args=[conversation.pk]),
            {"body": "Hello"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Message.objects.filter(conversation=conversation, sender=self.user, body="Hello").exists())

    def test_non_participant_redirected_from_conversation(self):
        third = User.objects.create_user(email="third@example.com", password="pass1234")
        conversation = Conversation.objects.create(user1=self.user, user2=self.other)
        self.client.login(email="third@example.com", password="pass1234")
        response = self.client.get(reverse("messaging:conversation", args=[conversation.pk]), follow=True)
        self.assertRedirects(response, reverse("messaging:inbox"))
