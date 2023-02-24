from drf_yasg import openapi


def get_social_auth_query_params():
    mock = openapi.Parameter('mock', openapi.IN_QUERY, description="For mock data", type=openapi.TYPE_STRING,
                             required=False, default="false", enum=["true", "false"])

    return [mock]


social_auth_query_params = get_social_auth_query_params()

social_auth_schema_body = openapi.Schema(
    name='body',
    description="Social Authentication",
    type=openapi.TYPE_OBJECT,
    properties={
        "access_token_key": openapi.Schema(type=openapi.TYPE_STRING),
        'access_token_secret': openapi.Schema(type=openapi.TYPE_STRING),
    }
)


social_auth_schema = {
    "200": openapi.Response(
        description="Social auth",
        schema=social_auth_schema_body
    ),
}
