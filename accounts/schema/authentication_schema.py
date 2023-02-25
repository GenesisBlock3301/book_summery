from drf_yasg import openapi

user_register_schema_body = openapi.Schema(
    name='body',
    description="User Register",
    type=openapi.TYPE_OBJECT,
    properties={
        "email": openapi.Schema(type=openapi.TYPE_STRING),
        "username": openapi.Schema(type=openapi.TYPE_STRING),
        'password': openapi.Schema(type=openapi.TYPE_STRING)
    }
)


user_register_schema = {
    "200": openapi.Response(
        description="User Register",
        schema=user_register_schema_body
    ),
}