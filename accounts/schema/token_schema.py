from drf_yasg import openapi


def get_token_query_params():
    token = openapi.Parameter('token', in_=openapi.IN_QUERY, description="Token params",
                              type=openapi.TYPE_STRING)
    return [token]


token_query_params = get_token_query_params()
