import os
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from .google import Google
from .register import register_social_user


class GoogleAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    @staticmethod
    def validate_auth_token(auth_token):
        user_data = Google.validate(auth_token)
        try:
            user_data["sub"]
        except:
            raise serializers.ValidationError(
                "The token invalid or expired. Please login again..."
            )

        if user_data["aud"] != os.environ.get("GOOGLE_CLIENT_ID"):
            raise AuthenticationFailed("Who are you?")

        # user_id = user_data["sub"]
        email = user_data["email"]
        name = user_data['name']
        provider = "google"

        return register_social_user(provider, email, name)
