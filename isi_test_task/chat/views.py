from django.shortcuts import render
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
)

from .models import *
from .serializers import ThreadSerializer

# Create your views here.


class ThreadApiView(ListAPIView):
    serializer_class = ThreadSerializer
    queryset = Thread.objects.all()


class TheThreadApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = ThreadSerializer
    queryset = Thread.objects.all()


# class
