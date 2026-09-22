from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, srn, email, password=None, **extra_fields):
        if not srn:
            raise ValueError('SRN is required')
        if not email:
            raise ValueError('Email is required')

        email = self.normalize_email(email)
        user = self.model(
            srn=srn,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, srn, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'SPORTS_ADMIN')

        return self.create_user(srn, email, password, **extra_fields)


class User(AbstractUser):
    username = None
    
    ROLE_CHOICES = [
        ('STUDENT', 'Student'),
        ('CAPTAIN', 'Captain'),
        ('COACH', 'Coach'),
        ('SPORTS_ADMIN', 'Sports Admin'),
    ]

    srn = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150, default="")
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='STUDENT'
    )

    objects = UserManager()

    USERNAME_FIELD = 'srn'
    REQUIRED_FIELDS = ['email', 'full_name']

    def __str__(self):
        if self.full_name:
            return f"{self.full_name} ({self.srn})"
        return self.srn