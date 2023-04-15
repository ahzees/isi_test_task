from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Thread


class ThreadTestCase(TestCase):
    def setUp(self):
        # Створюємо двох користувачів для тесту
        self.user1 = User.objects.create(username="user1")
        self.user2 = User.objects.create(username="user2")
        self.user3 = User.objects.create(username="user3")

    def test_thread_participants_limit(self):
        # Створюємо новий тред з двома учасниками
        thread = Thread.objects.create()
        thread.participants.add(self.user1, self.user2)
        # Спробуємо додати ще одного учасника до треду, має викликати помилку валідації
        with self.assertRaises(ValidationError):
            thread.participants.add(self.user3)
