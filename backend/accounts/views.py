import logging
import re
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status
from rest_framework.generics import ListAPIView
# from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from .schema.authentication_schema import user_register_schema_body
from .serializers import UserSerializer
from .schema.list_of_user import list_of_user_response

User = get_user_model()
logger = logging.getLogger(__name__)


class RegistrationView(APIView):
    """ User registration view"""
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def is_valid_email(email):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email) is not None

    @swagger_auto_schema(request_body=user_register_schema_body, tags=["auth"])
    def post(self, request):
        data = request.data
        username = data['username']
        password = data['password1']
        password2 = data['password2']
        if password == password2:
            if self.is_valid_email(username):
                if User.objects.filter(email=username).exists():
                    return Response({'error': 'Email already exists'})
                else:
                    if len(password) < 6:
                        return Response({'error': "Password must be at least 6 character"})
            else:
                return Response({"error": "Invalid Email Or Username"})
            user = User.objects.create_user(username=username, password=password)
            user.save()
            return Response({"status": "successfully registered"}, status=status.HTTP_200_OK)

        else:
            return Response({"status": "register failed"}, status=status.HTTP_400_BAD_REQUEST)


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(responses=list_of_user_response, tags=["users"])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
