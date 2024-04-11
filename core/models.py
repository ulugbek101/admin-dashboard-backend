from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom user model representing users in the system.

    This model extends Django's AbstractUser and includes additional fields for user status and profile information.

    Attributes:
        email (EmailField): The unique email address of the user.
        status (CharField): The status of the user, chosen from predefined choices.
        profile_image (ImageField): The profile image of the user, stored in the 'profile-images' directory.
        is_admin (BooleanField): Indicates whether the user is an admin.
        is_teacher (BooleanField): Indicates whether the user is a teacher.
        USERNAME_FIELD (str): The field used as the unique identifier for the user (email).
        REQUIRED_FIELDS (list): The fields required when creating a user.

    Methods:
        __str__(self): Returns the full name of the user.

    """

    class UserStatus(models.TextChoices):
        TEACHER = "teacher", "O'qituvchi"
        ADMIN = "admin", "Admin"
        SUPERUSER = "superuser", "Superadmin"

    email = models.EmailField(unique=True)
    status = models.CharField(max_length=10, choices=UserStatus.choices, default=UserStatus.TEACHER)
    profile_image = models.ImageField(default='profile-pictures/user-default.png', upload_to='profile-images/',
                                      blank=True)
    is_admin = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    def __str__(self):
        return self.get_full_name()
