from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .models import Message, Thread


# Ініціалізація даних для тестування
def create_user(username, email, password):
    return User.objects.create_user(username=username, email=email, password=password)


def create_thread(user1, user2):
    thread = Thread.objects.create()
    thread.participants.add(user1, user2)
    return thread


def create_message(sender, thread, text):
    return Message.objects.create(sender=sender, thread=thread, text=text)


# Тести для перегляду треду та створення треду
class ThreadApiViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = create_user("testuser1", "testuser1@gmail.com", "testpass")
        self.user2 = create_user("testuser2", "testuser2@gmail.com", "testpass")

    def test_create_thread(self):
        url = reverse("threads")
        data = {"user1_id": self.user1.pk, "user2_id": self.user2.pk}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_existing_thread(self):
        thread = create_thread(self.user1, self.user2)
        url = reverse("threads")
        data = {"user1_id": self.user1.pk, "user2_id": self.user2.pk}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_thread_with_same_user(self):
        url = reverse("threads")
        data = {"user1_id": self.user1.pk, "user2_id": self.user1.pk}
        response = self.client.post(url, data, format="json")
        self.assertEqual(len(response.data["participants"]), 1)


# Тести для видалення треду
class DeleteThreadApiViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = create_user("testuser1", "testuser1@gmail.com", "testpass")
        self.user2 = create_user("testuser2", "testuser2@gmail.com", "testpass")
        self.thread = create_thread(self.user1, self.user2)

    def test_delete_thread(self):
        url = reverse("threads-delete", args=[self.thread.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


# Тести для списку тредів користувача
class UserThreadsApiViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = create_user("testuser1", "testuser1@gmail.com", "testpass")
        self.user2 = create_user("testuser2", "testuser2@gmail.com", "testpass")
        self.user3 = create_user("testuser3", "testuser3@gmail.com", "testpass")
        self.thread = create_thread(self.user1, self.user2)
        self.thread = create_thread(self.user1, self.user3)

    def test_user_threads(self):
        url = reverse("user-threads", args=[self.user1.pk])
        response = self.client.get(url)
        self.assertEqual(len(response.data["threads"]), 2)
