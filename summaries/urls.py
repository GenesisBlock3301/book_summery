from django.urls import path

from .views import SummaryApiView, CreateCommentAPIView, UpdateCommentAPIView, GetSingleSummary, CreateReplyAPIView,\
    UpdateReplyAPIView

urlpatterns = [
    path('', SummaryApiView.as_view(), name="summaries"),
    path('<int:pk>/', GetSingleSummary.as_view(), name="get_single_summary"),
    path("comment/", CreateCommentAPIView.as_view(), name="create_comment"),
    path("comment/<pk>/", UpdateCommentAPIView.as_view(), name="update_comment"),
    path("reply/", CreateReplyAPIView.as_view(), name="create_reply"),
    path("reply/<pk>/", UpdateReplyAPIView.as_view(), name="update_reply")
]
