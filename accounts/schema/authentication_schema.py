from drf_yasg import openapi

user_register_schema_body = openapi.Schema(
    name='body',
    description="User Register",
    type=openapi.TYPE_OBJECT,
    properties={
        "username": openapi.Schema(type=openapi.TYPE_STRING),
        'password1': openapi.Schema(type=openapi.TYPE_STRING),
        'password2': openapi.Schema(type=openapi.TYPE_STRING),
    }
)


user_register_schema = {
    "200": openapi.Response(
        description="User Register",
        schema=user_register_schema_body
    ),
}