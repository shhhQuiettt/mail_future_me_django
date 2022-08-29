from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)


class UserManager(BaseUserManager):
    def _create_user(self, email, password, first_name, **other_fields):
        if not email:
            raise ValueError("Email must be provided")
        if not password:
            raise ValueError("Password must be provided")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            **other_fields,
        )

        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, first_name, **other_fields):
        other_fields.setdefault("is_staff", False)
        other_fields.setdefault("is_active", False)
        other_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, first_name, **other_fields)

    def create_superuser(self, email, password, first_name, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_active", True)
        other_fields.setdefault("is_superuser", True)

        return self._create_user(email, password, first_name, **other_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=254)
    first_name = models.CharField(max_length=127, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    is_active = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name"]

    def __str__(self):
        return (
            f"{self.email} ({self.first_name})" if self.first_name != "" else self.email
        )

    @property
    def email_count(self):
        return self.emailmessage_set.count()
