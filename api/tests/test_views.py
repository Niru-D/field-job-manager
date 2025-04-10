from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch
from ..constants import constant
from .test_utils import create_user_and_get_token, get_authenticated_client
from django.contrib.auth import get_user_model

User = get_user_model()


class MockToken:
    def __init__(self, key='mock-token-key'):
        self.key = key


class TestUserRegisterView(APITestCase):

    def setUp(self):
        self.url = reverse('user_register')
        self.valid_data = {
            'email': 'test@example.com',
            'password': 'SecurePassword123'
        }
        self.invalid_data = {
            'email': 'invalid-email',
            'password': ''
        }

    def test_register_user_success(self):
        response = self.client.post(self.url, self.valid_data, format='json')
        response_content = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response_content)
        self.assertEqual(response_content['message'], constant["UserCreationSuccess"])

    def test_register_user_invalid_data(self):
        response = self.client.post(self.url, self.invalid_data, format='json')
        response_content = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response_content)
        self.assertEqual(response_content['message'], constant["BadRequest"])

    @patch('api.services.user_services.CreateUser.execute')
    def test_register_user_exception(self, mock_execute):
        mock_execute.side_effect = Exception('Unexpected error')
        response = self.client.post(self.url, self.valid_data, format='json')
        response_content = response.json()
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response_content['message'], constant["SomethingWentWrong"])
        self.assertIn('Unexpected error', response_content['error'])


class TestUserLoginView(APITestCase):
    def setUp(self):
        self.url = reverse('user_login')
        self.valid_data = {
            'email': 'test@example.com',
            'password': 'SecurePassword123'
        }
        self.missing_email_data = {
            'password': 'SecurePassword123'
        }
        self.missing_password_data = {
            'email': 'test@example.com'
        }
        self.invalid_credentials_data = {
            'email': 'test@example.com',
            'password': 'WrongPassword'
        }

    @patch('api.services.user_services.LoginUser.execute')
    def test_login_success(self, mock_execute):
        mock_execute.return_value = MockToken()
        response = self.client.post(self.url, self.valid_data, format='json')
        response_content = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_content['message'], constant["UseLoginSuccess"])
        self.assertIn('token', response_content)
        self.assertEqual(response_content['token'], MockToken().key)

    def test_login_missing_fields(self):
        response = self.client.post(self.url, self.missing_email_data, format='json')
        response_content = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_content['message'], constant["BadRequest"])
        self.assertIn('Missing fields: email', response_content['error'])

        response = self.client.post(self.url, self.missing_password_data, format='json')
        response_content = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_content['message'], constant["BadRequest"])
        self.assertIn('Missing fields: password', response_content['error'])

    @patch('api.services.user_services.LoginUser.execute')
    def test_login_incorrect_credentials(self, mock_execute):
        mock_execute.return_value = None
        response = self.client.post(self.url, self.invalid_credentials_data, format='json')
        response_content = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response_content['message'], constant["IncorrectCredentials"])

    @patch('api.services.user_services.LoginUser.execute')
    def test_login_exception(self, mock_execute):
        mock_execute.side_effect = Exception('Unexpected error')
        response = self.client.post(self.url, self.valid_data, format='json')
        response_content = response.json()
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response_content['message'], constant["SomethingWentWrong"])
        self.assertIn('Unexpected error', response_content['error'])


class TestUserLogoutView(APITestCase):

    def setUp(self):
        self.url = reverse('user_logout')
        self.valid_data = {
            'email': 'test@example.com'
        }
        self.missing_email_data = {}
        self.user, self.token = create_user_and_get_token()
        self.client = get_authenticated_client(self.token.key)

    @patch('api.services.user_services.LogoutUser.execute')
    def test_logout_success(self, mock_execute):
        mock_execute.return_value = True
        response = self.client.post(self.url, self.valid_data, format='json')
        response_content = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_content['message'], constant["LogoutSuccess"])

    def test_logout_missing_email(self):
        response = self.client.post(self.url, self.missing_email_data, format='json')
        response_content = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_content['message'], constant["BadRequest"])

    @patch('api.services.user_services.LogoutUser.execute')
    def test_logout_failure(self, mock_execute):
        mock_execute.return_value = False
        response = self.client.post(self.url, self.valid_data, format='json')
        response_content = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_content['message'], constant["LogoutFailed"])

    @patch('api.services.user_services.LogoutUser.execute')
    def test_logout_exception(self, mock_execute):
        mock_execute.side_effect = Exception('Unexpected error')
        response = self.client.post(self.url, self.valid_data, format='json')
        response_content = response.json()
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response_content['message'], constant["SomethingWentWrong"])
        self.assertIn('Unexpected error', response_content['error'])


class TestJobsView(APITestCase):

    def setUp(self):
        self.url = reverse('jobs')
        self.valid_job_data = {
              "job_type": "SNOW_REMOVAL",
              "job_address": "67A, Cornwall North, Shire",
              "user": 1
        }
        self.invalid_job_data = {
            "job_type": "",
            "job_address": "",
            "user": 1
        }
        self.user, self.token = create_user_and_get_token()
        self.client = get_authenticated_client(self.token.key)

    @patch('api.services.job_services.CreateJob.execute')
    def test_create_job_success(self, mock_execute):
        mock_execute.return_value = None
        response = self.client.post(self.url, self.valid_job_data, format='json')
        response_content = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_content['message'], constant['SuccessJobCreation'])

    def test_create_job_invalid_data(self):
        response = self.client.post(self.url, self.invalid_job_data, format='json')
        response_content = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response_content)
        self.assertEqual(response_content['message'], constant["BadRequest"])

    @patch('api.services.job_services.CreateJob.execute')
    def test_create_job_exception(self, mock_execute):
        mock_execute.side_effect = Exception('Unexpected error')
        response = self.client.post(self.url, self.valid_job_data, format='json')
        response_content = response.json()
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response_content['message'], constant["SomethingWentWrong"])
        self.assertIn('Unexpected error', response_content['error'])

    @patch('api.services.job_services.FetchJobList.execute')
    def test_get_jobs_success(self, mock_execute):
        mock_execute.return_value = [{
            "id": 1,
            "job_type": "SNOW_REMOVAL",
            "job_address": "67A, Cornwall North, Shire",
            "status": "TODO",
            "finished_date": '2023-08-15T10:30:00',
            "user": 1
        }]
        response = self.client.get(self.url)
        response_content = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_content, [{
            "id": 1,
            "job_type": "SNOW_REMOVAL",
            "job_address": "67A, Cornwall North, Shire",
            "status": "TODO",
            "finished_date": '2023-08-15T10:30:00',
            "user": 1
        }])

    @patch('api.services.job_services.FetchJobList.execute')
    def test_get_jobs_no_jobs(self, mock_execute):
        mock_execute.return_value = []
        response = self.client.get(self.url)
        response_content = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_content['message'], constant['NoJobs'])

    @patch('api.services.job_services.FetchJobList.execute')
    def test_get_jobs_exception(self, mock_execute):
        mock_execute.side_effect = Exception('Unexpected error')
        response = self.client.get(self.url)
        response_content = response.json()
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response_content['message'], constant["SomethingWentWrong"])
        self.assertIn('Unexpected error', response_content['error'])


