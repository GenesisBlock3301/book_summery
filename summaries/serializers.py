from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from accounts.serializers import UserSerializer
from .models import Summary, Reply, Comment, Author


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class ReplySerializer(ModelSerializer):
    class Meta:
        model = Reply
        fields = "__all__"


class CommentSerializer(ModelSerializer):
    reply_set = ReplySerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"


class SummarySerializer(ModelSerializer):
    class Meta:
        model = Summary
        fields = "__all__"


class GetAllDetailSummarySerializer(ModelSerializer):
    comment_set = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Summary
        fields = "__all__"


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["user", "summary", "comment_content"]


class CreateReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["user", "comment", "reply_content"]
