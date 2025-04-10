from django.urls import path
from .views import JobsView, JobDetailView, RemoveFinishedJobsView, UserRegisterView, UserLoginView, UserLogoutView

urlpatterns = [
    path(
        "users/register",
        UserRegisterView.as_view(),
        name="user_register"
    ),
    path(
        "users/login",
        UserLoginView.as_view(),
        name="user_login"
    ),
    path(
        "users/logout",
        UserLogoutView.as_view(),
        name="user_logout"
    ),
    path(
        "jobs/",
        JobsView.as_view(),
        name="jobs",
    ),
    path(
        "jobs/<int:job_id>",
        JobDetailView.as_view(),
        name="job_detail",
    ),
    path(
        "jobs/delete_done/",
        RemoveFinishedJobsView.as_view(),
        name="remove_finished_jobs",
    )
]
