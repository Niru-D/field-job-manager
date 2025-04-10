from service_objects.services import Service
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User = get_user_model()


class CreateUser(Service):
    def process(self):
        serializer = self.data.get("serializer")
        serializer.save()
        user = User.objects.get(email=self.data.get("email"))
        user.set_password(self.data.get("password"))
        user.save()
        token = Token.objects.create(user=user)
        return token


class LoginUser(Service):
    def process(self):
        try:
            user = User.objects.get(email=self.data.get("email"))
        except User.DoesNotExist:
            return None
        if not user.check_password(self.data.get("password")):
            return None
        token, created = Token.objects.get_or_create(user=user)
        return token


class LogoutUser(Service):
    def process(self):
        try:
            user = User.objects.get(email=self.data.get("email"))
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            return None
        token.delete()
        return True