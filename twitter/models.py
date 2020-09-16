from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from fernet_fields import EncryptedTextField
from django.utils import timezone

# Create your models here.


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email must be provided')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be a Staff')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must not be have superuser set to True')
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField('Email Address', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Integration(models.Model):
    token = EncryptedTextField()
    secret = EncryptedTextField()
    profile_name = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class Post(models.Model):
    content = models.TextField(max_length=280)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=False)

    def __str__(self):
        return self.content


class History(models.Model):
    content = models.TextField()
    posted_time = models.DateTimeField('Posted Time', default=timezone.now)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.content
