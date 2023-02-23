from rest_framework.serializers import ModelSerializer
from .models import Summary


class SummarySerializer(ModelSerializer):
    class Meta:
        model = Summary
        fields = "__all__"

