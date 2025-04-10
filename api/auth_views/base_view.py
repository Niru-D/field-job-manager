from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from .bearer_token_auth import BearerTokenAuthentication


class BaseView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]


class AuthOnlyView(APIView):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]
