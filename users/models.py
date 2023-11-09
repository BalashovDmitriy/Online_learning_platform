from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=25, **NULLABLE)
    city = models.CharField(max_length=100, **NULLABLE)
    avatar = models.ImageField(upload_to="avatars", **NULLABLE)
    last_token_request = models.DateTimeField(**NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
