from django.test import TestCase
from unittest.mock import patch, MagicMock
from django.contrib.auth import get_user_model
from ..services.user_services import CreateUser

User = get_user_model()


class TestCreateUserService(TestCase):

    @patch('api.services.user_services.Token.objects.create')
    @patch('api.services.user_services.User.objects.get')
    def test_process_success(self, mock_get_user, mock_create_token):
        mock_user = MagicMock()
        mock_user.set_password = MagicMock()
        mock_user.save = MagicMock()
        mock_get_user.return_value = mock_user

        mock_token = MagicMock()
        mock_create_token.return_value = mock_token

        mock_serializer = MagicMock()
        mock_serializer.save = MagicMock()

        service = CreateUser(data={
            "serializer": mock_serializer,
            "email": "test@example.com",
            "password": "securePassword"
        })
        token = service.process()

        self.assertEqual(token, mock_token)
        mock_get_user.assert_called_once_with(email="test@example.com")
        mock_create_token.assert_called_once_with(user=mock_user)
        mock_user.set_password.assert_called_once_with("securePassword")
        mock_user.save.assert_called_once()
