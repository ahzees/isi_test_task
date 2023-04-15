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


# Створення класу, який буде містити метод для jwt автентифікації, і буде наслідуватись від всіх іншиї тест-кейсів
class JWTApiViewTestCase(APITestCase):
    def auth(self, user):
        data = {"username": user.username, "password": "testpass"}
        url = reverse("token_obtain_pair")
        response = self.client.post(url, data)
        return {"HTTP_AUTHORIZATION": f"Bearer {response.data['access']}"}


# Тести для перегляду треду та створення треду
class ThreadApiViewTestCase(JWTApiViewTestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = create_user("testuser1", "testuser1@gmail.com", "testpass")
        self.user2 = create_user("testuser2", "testuser2@gmail.com", "testpass")

    def test_create_thread(self):
        # Перевірка створення треду
        url = reverse("threads")
        data = {"user1_id": self.user1.pk, "user2_id": self.user2.pk}
        response = self.client.post(url, data, format="json", **self.auth(self.user1))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_existing_thread(self):
        # Перевірка створення треду з користувачами, що вже мають спільний тред
        thread = create_thread(self.user1, self.user2)
        url = reverse("threads")
        data = {"user1_id": self.user1.pk, "user2_id": self.user2.pk}
        response = self.client.post(url, data, format="json", **self.auth(self.user1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_thread_with_same_user(self):
        # Перевірка створення треду, якщо вказати 2-х однакових юзерів
        url = reverse("threads")
        data = {"user1_id": self.user1.pk, "user2_id": self.user1.pk}
        response = self.client.post(url, data, format="json", **self.auth(self.user1))
        self.assertEqual(len(response.data["participants"]), 1)


# Тести для видалення треду
class DeleteThreadApiViewTestCase(JWTApiViewTestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = create_user("testuser1", "testuser1@gmail.com", "testpass")
        self.user2 = create_user("testuser2", "testuser2@gmail.com", "testpass")
        self.thread = create_thread(self.user1, self.user2)

    def test_delete_thread(self):
        # перевірка видалення треду
        url = reverse("threads-delete", args=[self.thread.pk])
        response = self.client.delete(url, **self.auth(self.user1))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


# Тести для списку тредів користувача
class UserThreadsApiViewTestCase(JWTApiViewTestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = create_user("testuser1", "testuser1@gmail.com", "testpass")
        self.user2 = create_user("testuser2", "testuser2@gmail.com", "testpass")
        self.user3 = create_user("testuser3", "testuser3@gmail.com", "testpass")
        self.thread = create_thread(self.user1, self.user2)
        self.thread = create_thread(self.user1, self.user3)

    def test_user_threads(self):
        # Перевірка отримання всіх тредів для конкретного користувача
        url = reverse("user-threads", args=[self.user1.pk])
        response = self.client.get(url, **self.auth(self.user1))
        self.assertEqual(len(response.data["threads"]), 2)


# Тасти для повідомлень
class MessageApiViewTestCase(JWTApiViewTestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = create_user("testuser1", "testuser1@gmail.com", "testpass")
        self.user2 = create_user("testuser2", "testuser2@gmail.com", "testpass")
        self.thread = create_thread(self.user1, self.user2)
        self.message1 = create_message(self.user1, self.thread, "Hello")
        self.message2 = create_message(self.user2, self.thread, "Hi")

    def test_list_messages(self):
        # Превірка чи тред містить всі повідомлення
        url = reverse("threads-messages", args=[self.thread.pk])
        response = self.client.get(url, **self.auth(self.user1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_message(self):
        # Перевірка створення повідомлення для треду
        url = reverse("threads-messages", args=[self.thread.pk])
        data = {"text": "New message", "sender": self.user1.pk}
        response = self.client.post(url, data, format="json", **self.auth(self.user1))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["sender"], self.user1.pk)
        self.assertEqual(response.data["text"], "New message")

    def test_create_message_without_auth(self):
        # Перевірка створення повідомлення, якщо користувача не авторизовано
        url = reverse("threads-messages", args=[self.thread.pk])
        data = {"text": "New message"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
