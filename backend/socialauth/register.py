import os
import random
from django.contrib.auth import authenticate
from django.db.models import Q
from accounts.models import User


def generate_username(name):
    username = "".join(name.split(" ")).lower()
    if not User.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0,1000))
        return generate_username(random_username)


def register_social_user(provider, email, name):
    # generated_name = generate_username(name)
    params = Q(email=email) | Q(username=name)
    filter_user_email_or_name = User.objects.filter(params)

    if filter_user_email_or_name.exists():
        if provider == filter_user_email_or_name[0].provider:
            registered_user = authenticate(
                username=email, password=os.environ.get('SOCIAL_SECRET')
            )

            return {
                'username': registered_user.username,
                'email': registered_user.email,
                'tokens': registered_user.tokens()
            }
        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filter_user_email_or_name[0].auth_provider)
    else:
        user = {
            "username": generate_username(name),
            "email": email,
            "password": os.environ.get("SOCIAL_SECRET")
        }
        user = User.objects.create_user(**user)
        user.auth_provider = provider
        user.save()
        new_user = authenticate(
            email=email, password=os.environ.get('SOCIAL_SECRET'))
        return {
            'email': new_user.email,
            'username': new_user.username,
            'tokens': new_user.tokens(),
        }
