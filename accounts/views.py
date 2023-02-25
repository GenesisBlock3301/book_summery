import logging
import re

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status, generics
from rest_framework.generics import ListAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from .schema.authentication_schema import user_register_schema_body
from .schema.token_schema import token_query_params
from .serializers import UserSerializer
from .serializers import RegistrationSerializer
from .schema.list_of_user import list_of_user_response
from .renderers import UserRenderer
from summaries.pagination import CustomPagination
from .utils import Utils

User = get_user_model()
logger = logging.getLogger(__name__)


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
        Utils.send_email(data)
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


class VerifyEmail(APIView):

    @swagger_auto_schema(manual_parameters=token_query_params)
    def get(self, request):
        token = request.GET.get("token")
        try:
            # retrieve `token` from url's query_params
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.filter(id=payload["user_id"]).first()
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({"email": 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({"error": "Activated expired"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

