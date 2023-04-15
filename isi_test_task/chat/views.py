from django.contrib.auth.models import User
from django.db.models import Case, Count, When
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import (
    DestroyAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
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
    permission_classes = [
        IsAuthenticated,
    ]

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
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Якщо тред не існує, створюємо новий
        thread = Thread.objects.create()
        thread.participants.add(user1_id, user2_id)

        serializer = ThreadSerializer(thread)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Видалення треду
class DeleteThreadApiView(DestroyAPIView):
    serializer_class = TheThreadSerializer
    queryset = Thread.objects.all()
    permission_classes = [
        IsAuthenticated,
    ]


# Список тредів для конкретного користувача
class UserThreadsApiView(RetrieveAPIView):
    serializer_class = UserThreadSerializer
    queryset = User.objects.all()
    pagination_class = LimitOffsetPagination
    permission_classes = [
        IsAuthenticated,
    ]


# Список повідомлень для конкретного треду та створення нових
class ThreadMessagesApiView(ListCreateAPIView):
    serializer_class = ThreadMessagesSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [
        IsAuthenticated,
    ]

    # вибір всіх повідомлень для конкретного треду
    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Thread.objects.get(pk=pk).messages.all()

    # створення повідомлення для конкретного треду
    def post(self, request, *args, **kwargs):
        data = request.data
        thread = Thread.objects.get(pk=self.kwargs["pk"])
        if data["sender"] not in [i[0] for i in thread.participants.values_list("pk")]:
            return Response(
                ThreadMessagesSerializer(thread.messages.all(), many=True).data,
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )
        data["thread"] = thread.pk
        serializer = MessagesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


# Перегляд нових повідомлень для конкретного юзера
class NewUserMessagesApiView(APIView):
    serializer_class = UserThreadSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    # вибірка всіх повідомлень для конкретного юзера
    def get(self, request, pk):
        obj = get_object_or_404(User, pk=pk)
        count = (
            Message.objects.filter(is_read=False)
            .filter(thread__participants=obj)
            .exclude(sender=obj)
            .count()
        )
        return Response({"amount of new messages": count})


# Відмітити повідомлення як прочитане
class ReadMessageApiView(RetrieveUpdateAPIView):
    serializer_class = ViewMessagesSerializer
    queryset = Message.objects.all()
    permission_classes = [
        IsAuthenticated,
    ]
