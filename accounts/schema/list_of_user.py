from drf_yasg import openapi
from accounts.serializers import UserSerializer


list_of_user_schema_body = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    items=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "id": openapi.Schema(type=openapi.TYPE_NUMBER),
            "email": openapi.Schema(type=openapi.TYPE_STRING)
        }
    )
)

list_of_user_response = {
    "200": openapi.Response(
        description="User Register",
        schema=list_of_user_schema_body
    ),
}