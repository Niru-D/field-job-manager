from rest_framework import status
from django.http import JsonResponse
from .constants import constant
from .serializers.base_serializers import BaseResponseSerializer
from .serializers.model_serializers import JobSerializer, UserSerializer
from .services.job_services import FetchJobList, CreateJob, FetchJobInstance, UpdateJobStatus, RemoveFinishedJobs
from .services.user_services import CreateUser, LoginUser, LogoutUser
from .auth_views.base_view import AuthOnlyView, BaseView


class UserRegisterView(BaseView):

    @staticmethod
    def post(request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                token = CreateUser.execute({
                    "serializer": serializer,
                    "email": request.data['email'],
                    "password": request.data['password'],
                })
                return BaseResponseSerializer.register_success_response(
                    status.HTTP_201_CREATED,
                    constant["UserCreationSuccess"],
                    str(token)
                )
            else:
                return BaseResponseSerializer.error_response(
                    serializer.errors,
                    status.HTTP_400_BAD_REQUEST,
                    constant["BadRequest"]
                )

        except Exception as e:
            return BaseResponseSerializer.error_response(
                str(e),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                constant["SomethingWentWrong"],
            )


class UserLoginView(BaseView):

    @staticmethod
    def post(request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            if not email or not password:
                missing_fields = []
                if not email:
                    missing_fields.append('email')
                if not password:
                    missing_fields.append('password')
                return BaseResponseSerializer.error_response(
                    {f"Missing fields: {', '.join(missing_fields)}"},
                    status.HTTP_400_BAD_REQUEST,
                    constant["BadRequest"]
                )
            token = LoginUser.execute({
                "email": request.data['email'],
                "password": request.data['password'],
            })
            if not token:
                return BaseResponseSerializer.error_response(
                    constant["IncorrectCredentials"],
                    status.HTTP_401_UNAUTHORIZED,
                    constant["IncorrectCredentials"]
                )
            return BaseResponseSerializer.register_success_response(
                status.HTTP_200_OK,
                constant["UseLoginSuccess"],
                token.key
            )
        except Exception as e:
            return BaseResponseSerializer.error_response(
                str(e),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                constant["SomethingWentWrong"],
            )


class UserLogoutView(AuthOnlyView):

    @staticmethod
    def post(request):
        try:
            email = request.data.get('email')
            if not email:
                return BaseResponseSerializer.error_response(
                    constant["EmailMissing"],
                    status.HTTP_400_BAD_REQUEST,
                    constant["BadRequest"]
                )
            logout_success = LogoutUser.execute({
                "email": request.data['email']
            })
            if logout_success:
                return BaseResponseSerializer.success_response(
                    status.HTTP_200_OK,
                    constant["LogoutSuccess"],
                )
            else:
                return BaseResponseSerializer.error_response(
                    constant["LogoutFailed"],
                    status.HTTP_400_BAD_REQUEST,
                    constant["LogoutFailed"]
                )
        except Exception as e:
            return BaseResponseSerializer.error_response(
                str(e),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                constant["SomethingWentWrong"],
            )


class JobsView(AuthOnlyView):

    @staticmethod
    def post(request):
        try:
            serializer = JobSerializer(data=request.data)
            if serializer.is_valid():
                CreateJob.execute({
                    "serializer": serializer,
                })
                return BaseResponseSerializer.success_response(
                    status.HTTP_201_CREATED,
                    constant['SuccessJobCreation']
                )
            else:
                return BaseResponseSerializer.error_response(
                    serializer.errors,
                    status.HTTP_400_BAD_REQUEST,
                    constant["BadRequest"]
                )

        except Exception as e:
            return BaseResponseSerializer.error_response(
                str(e),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                constant["SomethingWentWrong"],
            )

    @staticmethod
    def get(request):
        try:
            print(request.data)
            jobs = FetchJobList.execute(inputs={})
            if jobs:
                return JsonResponse(jobs, status=status.HTTP_200_OK, safe=False)
            else:
                return BaseResponseSerializer.success_response(
                    status.HTTP_200_OK,
                    constant['NoJobs']
                )

        except Exception as e:
            return BaseResponseSerializer.error_response(
                str(e),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                constant["SomethingWentWrong"],
            )


class JobDetailView(AuthOnlyView):

    @staticmethod
    def get(request, job_id):
        try:
            job = FetchJobInstance.execute({
                "job_id": job_id
            })
            if job:
                job_data = JobSerializer(job).data
                return JsonResponse(job_data, status=status.HTTP_200_OK, safe=False)
            else:
                return BaseResponseSerializer.error_response(
                    constant['JobNotFound'],
                    status.HTTP_404_NOT_FOUND,
                    constant['JobNotFoundMsg']
                )
        except Exception as e:
            return BaseResponseSerializer.error_response(
                str(e),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                constant["SomethingWentWrong"],
            )

    @staticmethod
    def put(request, job_id):
        try:
            job = FetchJobInstance.execute({
                "job_id": job_id
            })
            if job:
                update_success = UpdateJobStatus.execute({
                    "job_instance": job,
                    "request_data": request.data
                })
                if update_success:
                    return BaseResponseSerializer.success_response(
                        status.HTTP_201_CREATED,
                        constant['SuccessJobUpdate']
                    )
                else:
                    return BaseResponseSerializer.error_response(
                        constant["UpdateFail"],
                        status.HTTP_400_BAD_REQUEST,
                        constant["BadRequest"]
                    )
            else:
                return BaseResponseSerializer.error_response(
                    constant['JobNotFound'],
                    status.HTTP_404_NOT_FOUND,
                    constant['JobNotFoundMsg']
                )
        except Exception as e:
            return BaseResponseSerializer.error_response(
                str(e),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                constant["SomethingWentWrong"],
            )


class RemoveFinishedJobsView(AuthOnlyView):

    @staticmethod
    def delete(request):
        try:
            remove_success_msg = RemoveFinishedJobs.execute(inputs={})
            return BaseResponseSerializer.success_response(
                status.HTTP_201_CREATED,
                remove_success_msg
            )
        except Exception as e:
            return BaseResponseSerializer.error_response(
                str(e),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                constant["SomethingWentWrong"],
            )