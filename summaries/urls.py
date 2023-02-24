from django.urls import path

from .views import SummaryApiView, CreateCommentAPIView, UpdateCommentAPIView, GetSingleSummary

urlpatterns = [
    path('', SummaryApiView.as_view()),
    path('<int:pk>/', GetSingleSummary.as_view()),
    path("comment/", CreateCommentAPIView.as_view()),
    path("comment/<pk>/", UpdateCommentAPIView.as_view())
]
