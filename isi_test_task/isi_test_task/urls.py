"""isi_test_task URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    re_path(r"^admin/", admin.site.urls),
    re_path("", include("chat.urls")),
    re_path(
        r"^api/token/$", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),  # url для авторизації та отримання jwt токена
    re_path(
        r"^api/token/refresh$",
        TokenRefreshView.as_view(),
        name="token_obtain_pair_refresh",
    ),  # url для оновлення jwt токена
    re_path(r"^__debug__/", include("debug_toolbar.urls")),
]
