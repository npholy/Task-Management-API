from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # This is a custom user model. 
    # The default fields from AbstractUser are already included.
    email = models.EmailField(unique=True)

    # The groups and user_permissions fields are explicitly defined to resolve the clash.
    # related_name is a crucial argument for solving the SystemCheckError.
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=('groups'),
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="custom_user_set",
        related_query_name="custom_user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=('user permissions'),
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_name="custom_user_permissions_set",
        related_query_name="custom_user_permission",
    )

    def __str__(self):
        return self.username