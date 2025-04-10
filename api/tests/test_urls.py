from rest_framework.test import APITestCase
from django.urls import resolve, reverse
from ..views import UserRegisterView, UserLoginView, UserLogoutView, JobsView, JobDetailView, RemoveFinishedJobsView


class TestUrlToView(APITestCase):
    """
    Test cases for testing urls.
    """

    def test_user_registration_url(self):
        url = reverse("user_register")
        response = resolve(url)
        self.assertEqual(response.func.cls, UserRegisterView)

    def test_user_login_url(self):
        url = reverse("user_login")
        response = resolve(url)
        self.assertEqual(response.func.cls, UserLoginView)

    def test_user_logout_url(self):
        url = reverse("user_logout")
        response = resolve(url)
        self.assertEqual(response.func.cls, UserLogoutView)

    def test_jobs_url(self):
        url = reverse("jobs")
        response = resolve(url)
        self.assertEqual(response.func.cls, JobsView)

    def test_job_detail_url(self):
        url = reverse("job_detail", kwargs={"job_id": 1})
        response = resolve(url)
        self.assertEqual(response.func.cls, JobDetailView)

    def test_remove_finished_jobs_url(self):
        url = reverse("remove_finished_jobs")
        response = resolve(url)
        self.assertEqual(response.func.cls, RemoveFinishedJobsView)

    # Ensure that named URLs are correctly reversing to the expected paths

    def test_reverse_user_registration_url(self):
        url = reverse("user_register")
        self.assertEqual(url, "/api/users/register")
