from django.urls import path
from .views import RegistrationView, UserListView


urlpatterns = [
    path('register/', RegistrationView.as_view(), name="register"),
    path("users/", UserListView.as_view(), name="user_list")
]
