from django.urls import path

from . import views

urlpatterns = [
    path(
        "api/threads/", views.ThreadApiView.as_view(), name="threads"
    ),  # Перегляд треду та Створення треду
    path(
        "api/threads/<int:pk>/",
        views.DeleteThreadApiView.as_view(),
        name="threads-delete",
    ),  # Видалення треду
    path(
        "api/threads/<int:pk>/messages/",
        views.ThreadMessagesApiView.as_view(),
        name="threads-messages",
    ),  # Перегляд всіх повідомлень в треді та створення нового повідомлення
    path(
        "api/users/<int:pk>/threads/",
        views.UserThreadsApiView.as_view(),
        name="user-threads",
    ),  # Перегляд всіх тредів конкретного користувача
    path(
        "api/users/<int:pk>/new_messages/",
        views.NewUserMessagesApiView.as_view(),
        name="user-new-messages",
    ),  # Перегляд всіх непрочитаних повідомлень для конкретного юзера
    path(
        "api/messages/<int:pk>/",
        views.ReadMessageApiView.as_view(),
        name="message-read",
    ),  # Прочитати повідомлення
]
