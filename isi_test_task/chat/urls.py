from django.urls import path, re_path

from . import views

urlpatterns = [
    re_path(
        r"^api/threads/$", views.ThreadApiView.as_view(), name="threads"
    ),  # Перегляд треду та Створення треду
    re_path(
        r"^api/threads/(?P<pk>\d+)/$",
        views.DeleteThreadApiView.as_view(),
        name="threads-delete",
    ),  # Видалення треду
    re_path(
        r"^api/threads/(?P<pk>\d+)/messages/$",
        views.ThreadMessagesApiView.as_view(),
        name="threads-messages",
    ),  # Перегляд всіх повідомлень в треді та створення нового повідомлення
    re_path(
        r"^api/users/(?P<pk>\d+)/threads/$",
        views.UserThreadsApiView.as_view(),
        name="user-threads",
    ),  # Перегляд всіх тредів конкретного користувача
    re_path(
        r"^api/users/(?P<pk>\d+)/new_messages/$",
        views.NewUserMessagesApiView.as_view(),
        name="user-new-messages",
    ),  # Перегляд всіх непрочитаних повідомлень для конкретного юзера
    re_path(
        r"api/messages/(?P<pk>\d+)/",
        views.ReadMessageApiView.as_view(),
        name="message-read",
    ),  # Прочитати повідомлення
]
