from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(
        self, email, password=None, registration_method="email", **extra_fields
    ):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(
            email=email, registration_method=registration_method, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, password=None, registration_method="email", **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, registration_method, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    registration_method = models.CharField(
        max_length=10,
        choices=[("email", "Email"), ("google", "Google")],
        default="email",
    )
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    blood_group = models.CharField(max_length=6, null=True, blank=True)
    image = models.ImageField(upload_to="images/users/", null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [] 

    objects = CustomUserManager()

    def __str__(self):
        return str(self.email)
