from drf_yasg import openapi


comment_schema_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "user": openapi.Schema(type=openapi.TYPE_INTEGER),
            "summary": openapi.Schema(type=openapi.TYPE_INTEGER),
            "comment_content": openapi.Schema(type=openapi.TYPE_STRING),
        }
)

