import logging
import jwt
import os
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http import HttpResponsePermanentRedirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics, permissions
from rest_framework.generics import ListAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from summaries.pagination import CustomPagination
from .renderers import UserRenderer
from .utils import Utils
from .schema.authentication_schema import user_register_schema_body, user_login_schema_body
from .schema.token_schema import token_query_params
from .serializers import UserSerializer
from .serializers import RegistrationSerializer, LoginSerializer, ResetPasswordEmailRequestSerializer, \
    SetNewPasswordSerializer, LogoutSerializer
from .schema.list_of_user import list_of_user_response
from .tasks import send_email_confirmation

User = get_user_model()
logger = logging.getLogger(__name__)


class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']


class RegistrationView(generics.GenericAPIView):
    """ User registration view"""
    serializer_class = RegistrationSerializer
    renderer_classes = (UserRenderer,)

    @swagger_auto_schema(request_body=user_register_schema_body)
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.filter(email=user_data["email"]).first()
        current_site = get_current_site(request).domain
        relative_link = reverse("email-verify")
        token = RefreshToken.for_user(user).access_token
        absurl = f"http://{current_site}{relative_link}?token={str(token)}"
        email_body = f"""
        Hi, {user.username} Use the link below to verify your email\n
        {absurl}
        """
        data = {
            "email_body": email_body, "to_email": user.email,
            "email_subject": "Verify your email"
        }
        # use celery for handling background task.
        send_email_confirmation.delay(data)
        return Response(user_data, status=status.HTTP_201_CREATED)


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(responses=list_of_user_response)
    def get(self, request, *args, **kwargs):
        # if in query parameter has _id then get single value.
        paginator = CustomPagination()
        query_set = User.objects.all()
        # Send queryset to paginator.
        result_page = paginator.get_queryset(data=query_set, request=request)
        # Again result page send to pagination for further response
        serializer = UserSerializer(result_page, many=True)
        return paginator.get_response(serializer.data)


class LoginApiView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    @swagger_auto_schema(request_body=user_login_schema_body)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VerifyEmail(APIView):

    @swagger_auto_schema(manual_parameters=token_query_params)
    def get(self, request):
        token = request.GET.get("token")
        try:
            # retrieve `token` from url's query_params
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.filter(id=payload["user_id"]).first()
            # user `is_verified` update here
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({"email": 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({"error": "Activated expired"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        # serializer = self.serializer_class(data=request.data)
        email = request.data.get("email", '')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request).domain
            relative_link = reverse("password-reset-confirm", kwargs={'uidb64': uid64, 'token': token})
            redirect_url = request.data.get("redirect_url", '')
            absurl = f"http://{current_site}{relative_link}"
            email_body = 'Hello, \n Use link below to reset your password  \n' + \
                         absurl + "?redirect_url=" + redirect_url
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your password'}
            Utils.send_email(data)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


class ResetPasswordTokenApiCheck(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):
        redirect_url = request.GET.get("redirect_url")
        try:
            # decode user id from uidb64
            _id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=_id)
            # check user's token is valid or not
            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    # redirect to custom schem based url
                    return CustomRedirect(redirect_url + '?token_valid=False')
                else:
                    return CustomRedirect(os.environ.get("FRONTEND_URL", '') + "?token_valid=False")
            if redirect_url and len(redirect_url) > 3:
                return CustomRedirect(redirect_url + "?token_valid=True&message=Credentials Valid&uidb64="
                                      + uidb64 + "&token=" + token)
            else:
                return CustomRedirect(os.environ.get('FRONTEND_URL', '') + '?token_valid=False')
        except DjangoUnicodeDecodeError:
            try:
                _id = smart_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(id=_id)
                if not PasswordResetTokenGenerator().check_token(user, token):
                    return CustomRedirect(redirect_url + '?token_valid=False')
            except UnboundLocalError as e:
                return Response({'error': 'Token is not valid, please request a new one'},
                                status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
