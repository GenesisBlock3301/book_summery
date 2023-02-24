from drf_yasg import openapi


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
            "user": openapi.Schema(type=openapi.TYPE_INTEGER),
            "author": openapi.Schema(type=openapi.TYPE_INTEGER),
            "book_title": openapi.Schema(type=openapi.TYPE_STRING),
            "summary_content": openapi.Schema(type=openapi.TYPE_STRING),
            "is_like": openapi.Schema(type=openapi.TYPE_BOOLEAN),
        }
    )
)

# Response schema
summary_response = {
    "200": openapi.Response(
        description="Summary list Response",
        schema=summary_schema_body
    ),
}


single_summary_schema_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "user": openapi.Schema(type=openapi.TYPE_INTEGER),
        "author": openapi.Schema(type=openapi.TYPE_INTEGER),
        "book_title": openapi.Schema(type=openapi.TYPE_STRING),
        "comment_set": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "user": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "summary": openapi.Schema(type=openapi.TYPE_STRING),
                    "comment_content": openapi.Schema(type=openapi.TYPE_STRING),
                    "is_like": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    "reply_set": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "user": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "comment": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "reply_content": openapi.Schema(type=openapi.TYPE_STRING),
                                "is_like": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            }
                        )
                    )
                }
            )
        )
    }
)

single_summary_response = {
    "200": openapi.Response(
        description="Single Summary Response",
        schema=single_summary_schema_body
    )
}
