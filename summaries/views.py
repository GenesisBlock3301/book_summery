import logging
from django.db.models import Prefetch
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .serializers import SummarySerializer, GetAllDetailSummarySerializer, CreateCommentSerializer
from summaries.schema.summary_schema import summary_response, summary_query_params,\
    single_summary_response
from summaries.schema.comment_schema import comment_schema_body
from .models import Summary, Comment, Reply
from .pagination import CustomPagination

logger = logging.getLogger(__name__)


class GetSingleSummary(APIView):
    @swagger_auto_schema(responses=single_summary_response)
    def get(self, request, pk):
        try:
            # Retrieve single Summary with corresponding comments and replies
            summary = Summary.objects.select_related("author", "user").filter(id=int(pk))\
                .prefetch_related(
                Prefetch('comment_set', queryset=Comment.objects.select_related("user").prefetch_related(
                    Prefetch("reply_set", queryset=Reply.objects.select_related("user"))
                ))
            ).first()
            serializer = GetAllDetailSummarySerializer(summary)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.critical(str(e), exc_info=True)
            Response(status=status.HTTP_400_BAD_REQUEST)


class SummaryApiView(APIView):

    @swagger_auto_schema(request_body=SummarySerializer)
    def post(self, request):
        data = request.data
        serializer = SummarySerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"status": "successfully create summary"}, status=status.HTTP_200_OK)
        return Response({"error": "failed to create summary"}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses=summary_response)
    def get(self, request):
        # if in query parameter has _id then get single value.
        paginator = CustomPagination()
        query_set = Summary.objects.select_related("author", "user").all()

        # Send queryset to paginator.
        result_page = paginator.get_queryset(data=query_set, request=request)
        # Again result page send to pagination for further response
        serializer = GetAllDetailSummarySerializer(result_page, many=True)
        return paginator.get_response(serializer.data)


class CreateCommentAPIView(APIView):
    @swagger_auto_schema(request_body=comment_schema_body)
    def post(self, request):
        try:
            data = request.data
            comment = Comment.objects.create(data)
            comment.save()
            Response({"status": "post create successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.critical(str(e), exc_info=True)
            return Response({"error": "post create failed"}, status=status.HTTP_400_BAD_REQUEST)


class UpdateCommentAPIView(APIView):
    @swagger_auto_schema(request_body=comment_schema_body)
    def put(self, request, pk):
        try:
            obj = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CreateCommentSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
