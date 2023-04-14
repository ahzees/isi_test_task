from django.urls import path

from . import views

urlpatterns = [
    path("api/threads/", views.ThreadApiView.as_view()),
    path("api/threads/<int:pk>", views.TheThreadApiView.as_view()),
]
