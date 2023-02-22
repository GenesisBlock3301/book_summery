from django.urls import path, include
from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = routers.DefaultRouter()

schema_view = get_schema_view(
    openapi.Info(
        title="Book Summery API",
        default_version="v1",
        description="""
        A book summary web app backend is a server-side component that provides functionality for a web application 
        that allows users to search for and view summaries of books. The backend typically includes a database for 
        storing book information, an API for querying the database and returning data to the frontend_, and business
         logic for handling user requests.
        """,
        terms_of_service="https://your-terms-of-service.com",
        contact=openapi.Contact(email="contact@your-company.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


# from drf_yasg.utils import swagger_auto_schema

# @swagger_auto_schema(
#     operation_summary="Your summary",
#     operation_description="Your description",
#     request_body=MySerializer,
#     responses={
#         status.HTTP_200_OK: MyResponseSerializer,
#         status.HTTP_400_BAD_REQUEST: "Bad request",
#     },
#     tags=['Your tag'],
# )
# def your_view_function(request):
# # ...