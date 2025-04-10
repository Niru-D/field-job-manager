from django.db import models
from django.contrib.auth import models as auth_models


class UserManager(auth_models.BaseUserManager):
    def create_user(self, email: str, password: str = None, is_staff: bool = False, is_superuser: bool = False) -> "User":
        if not email:
            raise ValueError('Users must have an email')

        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.is_active = True
        user.save()
        return user

    def create_superuser(self, email: str, password: str) -> "User":
        user = self.create_user(
            email=email,
            password=password,
            is_staff=True,
            is_superuser=True,
        )
        user.save()
        return user


class User(auth_models.AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=50)
    username = None

    def __str__(self):
        return self.email

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Job(models.Model):
    class JobType(models.TextChoices):
        LAWN_MOWING = 'LAWN_MOWING', 'Lawn Mowing'
        SNOW_REMOVAL = 'SNOW_REMOVAL', 'Snow Removal'
        SPRING_CLEANUP = 'SPRING_CLEANUP', 'Spring Cleanup'

    class JobStatus(models.TextChoices):
        TODO = 'TODO', 'Todo'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        DONE = 'DONE', 'Done'

    job_type = models.CharField(choices=JobType.choices, default=JobType.LAWN_MOWING, max_length=20)
    job_address = models.CharField(max_length=100)
    status = models.CharField(choices=JobStatus.choices, default=JobStatus.TODO, max_length=20)
    finished_date = models.DateTimeField(null=True, blank=True, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.job_type} at {self.job_address} is assigned to {self.user}"
