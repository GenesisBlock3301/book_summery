from django.urls import path
from .views import RegistrationView, UserListView, VerifyEmail


urlpatterns = [
    path('register/', RegistrationView.as_view(), name="register"),
    path("users/", UserListView.as_view(), name="user_list"),
    path("email-verify/", VerifyEmail.as_view(), name="email-verify")
]
