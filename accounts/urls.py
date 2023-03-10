from django.urls import path
from .views import RegistrationView, LoginApiView, UserListView, VerifyEmail, RequestPasswordResetEmail,\
    ResetPasswordTokenApiCheck, SetNewPasswordAPIView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('register/', RegistrationView.as_view(), name="register"),
    path('login/', LoginApiView.as_view(), name="login"),
    path("users/", UserListView.as_view(), name="user_list"),
    path("email-verify/", VerifyEmail.as_view(), name="email-verify"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("request-reset-email/", RequestPasswordResetEmail.as_view(), name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/',
         ResetPasswordTokenApiCheck.as_view(), name='password-reset-confirm'),
    path('password-reset-complete', SetNewPasswordAPIView.as_view(),
         name='password-reset-complete')
]
