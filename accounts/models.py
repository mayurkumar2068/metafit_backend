from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, mobile_number, full_name, email=None, **extra_fields):
        if not mobile_number:
            raise ValueError('mobile_number is required')
        if not full_name:
            raise ValueError('full_name is required')

        email = self.normalize_email(email) if email else None
        user = self.model(
            mobile_number=mobile_number.strip(),
            full_name=full_name.strip(),
            email=email,
            **extra_fields,
        )
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_number, full_name, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        user = self.create_user(
            mobile_number=mobile_number,
            full_name=full_name,
            email=email,
            **extra_fields,
        )
        if password:
            user.set_password(password)
            user.save(update_fields=['password'])
        return user


class User(AbstractBaseUser, PermissionsMixin):
    mobile_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    full_name = models.CharField(max_length=120)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return f'{self.full_name} ({self.mobile_number})'
