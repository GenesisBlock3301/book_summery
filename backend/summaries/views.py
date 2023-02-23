from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from drf_yasg.utils import swagger_auto_schema
from .serializers import SummarySerializer
from summaries.schema.list_of_summary_schema import summary_response, summary_query_params
from .models import Summary
from .pagination import CustomPagination


class SummaryApiView(APIView):
    
    @swagger_auto_schema(request_body=SummarySerializer, tags=["Summary"])
    def post(self, request):
        data = request.data
        serializer = SummarySerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"status": "successfully create summary"}, status=status.HTTP_200_OK)
        return Response({"error": "failed to create summary"}, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(manual_parameters=summary_query_params, responses=summary_response, tags=["Summary"])
    def get(self, request):
        # if in query parameter has _id then get single value.
        _id = request.query_params.get("_id", None)
        if _id:
            summary = Summary.objects.select_related("author", "user").filter(id=int(_id)).first()
            serializer = SummarySerializer(summary)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            paginator = CustomPagination()
            query_set = Summary.objects.select_related("author", "user").all()
            # Send queryset to paginator
            result_page = paginator.get_queryset(data=query_set, request=request)
            # Again result page send to pagination for further response
            serializer = SummarySerializer(result_page, many=True)
            return paginator.get_response(serializer.data)




