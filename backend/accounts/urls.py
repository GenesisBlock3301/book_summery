from django.contrib import admin
from django.urls import path, include
from rest_framework import routers, permissions
from .views import RegistrationView, UserListView


urlpatterns = [
    path('register/', RegistrationView.as_view(), name="register"),
    path("users/", UserListView.as_view(), name="user_list")
]
