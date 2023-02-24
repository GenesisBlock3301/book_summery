from drf_yasg import openapi
from accounts.serializers import UserSerializer


# Query parameter
def get_summary_query_params():
    _id = openapi.Parameter('_id', openapi.IN_QUERY, description="For get single summary", type=openapi.TYPE_INTEGER,
                            default=None)
    return [_id]


summary_query_params = get_summary_query_params()

# request body
summary_schema_body = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    items=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "user": openapi.Schema(type=openapi.TYPE_STRING),
            "author": openapi.Schema(type=openapi.TYPE_STRING),
            "book_title": openapi.Schema(type=openapi.TYPE_STRING),
            "summary_content": openapi.Schema(type=openapi.TYPE_STRING),
            "is_like": openapi.Schema(type=openapi.TYPE_BOOLEAN),
        }
    )
)

# Response schema
summary_response = {
    "200": openapi.Response(
        description="User Register",
        schema=summary_schema_body
    ),
}
