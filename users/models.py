from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Add extra fields if you want (e.g. role, profile photo, etc.)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username
