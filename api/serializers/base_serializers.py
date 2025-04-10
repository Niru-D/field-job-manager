from django.http import JsonResponse
from rest_framework import serializers


class BaseResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField(default=True)
    message = serializers.CharField()
    code = serializers.IntegerField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    @staticmethod
    def success_response(status, message):
        response_data = {
            "success": True,
            "status": status,
            "message": message
        }
        return JsonResponse(response_data, status=status)

    @staticmethod
    def error_response(error, status, message):
        response_data = {
            "success": False,
            "error": str(error),
            "status": status,
            "message": message
        }
        return JsonResponse(response_data, status=status)

    @staticmethod
    def register_success_response(status, message, token):
        response_data = {
            "success": True,
            "status": status,
            "message": message,
            "token": token
        }
        return JsonResponse(response_data, status=status)
