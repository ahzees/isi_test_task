from django.urls import path

from . import views

urlpatterns = [
    path(
        "api/threads/", views.ThreadApiView.as_view()
    ),  # Перегляд треду та Створення треду
    path(
        "api/threads/<int:pk>/", views.DeleteThreadApiView.as_view()
    ),  # Видалення треду
    path(
        "api/threads/<int:pk>/messages/", views.ThreadMessagesApiView.as_view()
    ),  # Перегляд всіх повідомлень в треді та створення нового повідомлення
]
