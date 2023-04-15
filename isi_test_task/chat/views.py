from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import (
    DestroyAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import (
    MessagesSerializer,
    TheThreadSerializer,
    ThreadMessagesSerializer,
    ThreadSerializer,
    UserThreadSerializer,
    ViewMessagesSerializer,
)


# Перегляд треду та Створення треду
class ThreadApiView(ListCreateAPIView):
    serializer_class = ThreadSerializer
    queryset = Thread.objects.all()

    def post(self, request):
        user1_id = get_object_or_404(User, pk=request.data.get("user1_id"))
        user2_id = get_object_or_404(User, pk=request.data.get("user2_id"))

        # Перевіряємо, чи вже існує тред для цих двох користувачів
        # Якщо тред існує, повертаємо його
        if (
            thread := Thread.objects.filter(participants=user1_id)
            .filter(participants=user2_id)
            .first()
        ):
            serializer = ThreadSerializer(thread)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Якщо тред не існує, створюємо новий
        thread = Thread.objects.create()
        thread.participants.add(user1_id, user2_id)
        thread.save()

        serializer = ThreadSerializer(thread)
        return Response(serializer.data)


# Видалення треду
class DeleteThreadApiView(DestroyAPIView):
    serializer_class = TheThreadSerializer
    queryset = Thread.objects.all()


# Список повідомлень для конкретного треду та створення нових
class ThreadMessagesApiView(ListCreateAPIView):
    serializer_class = ThreadMessagesSerializer

    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Thread.objects.get(pk=pk).messages.all()

    def post(self, request, *args, **kwargs):
        data = request.data
        if data["sender"] not in (
            thread := [
                i[0]
                for i in (
                    Thread.objects.get(pk=self.kwargs["pk"])
                ).participants.values_list("pk")
            ]
        ):
            return Response(
                ThreadMessagesSerializer(thread.messages.all(), many=True).data,
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )
        data["thread"] = self.kwargs["pk"]
        serializer = MessagesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
