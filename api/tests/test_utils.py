from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


def create_user_and_get_token(email='test@example.com', password='SecurePassword123'):
    user = User.objects.create_user(email=email, password=password)
    token, created = Token.objects.get_or_create(user=user)
    return user, token


def get_authenticated_client(token_key):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + token_key)
    return client
