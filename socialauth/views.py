from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import GoogleAuthSerializer
from drf_yasg.utils import swagger_auto_schema
from .schemas.social_auth_schema import social_auth_schema_body, social_auth_query_params


# Create your views here.
class GoogleSocialAuthView(APIView):
    serializer_class = GoogleAuthSerializer

    @swagger_auto_schema(
        manual_parameters=social_auth_query_params,
        request_body=social_auth_schema_body,
        tags=['SocialAuth'],
    )
    def post(self, request):
        """post with `auth_token`
        send an `id_token` as from Google to get user information
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data["auth_token"]
        return Response(data, status=status.HTTP_200_OK)
