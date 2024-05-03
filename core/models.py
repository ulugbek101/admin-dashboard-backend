from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.db.models.query import QuerySet


class UserManager(BaseUserManager):
    """
    Custom user manager for the CustomUser model.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular user with the given email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a superuser with the given email and password.
        """
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self.create_user(email, password, **extra_fields)


class SuperAdminManager(UserManager):
    def get_queryset(self) -> QuerySet:
        return User.objects.filter(is_superuser=True)


class AdminManager(UserManager):
    def get_queryset(self) -> QuerySet:
        return User.objects.filter(is_admin=True)


class TeacherManager(UserManager):
    def get_queryset(self) -> QuerySet:
        return User.objects.filter(is_teacher=True)


class StudentManager(UserManager):
    def get_queryset(self) -> QuerySet:
        return User.objects.filter(is_student=True)


class UserStatus(models.TextChoices):
    STUDENT = "student", "Student"
    TEACHER = "teacher", "Ustoz"
    ADMIN = "admin", "Admin"
    SUPERUSER = "superuser", "Superadmin"


class User(AbstractUser):
    """
    Custom user model to handle various user roles.
    """
    email = models.EmailField(unique=True)
    status = models.CharField(
        max_length=10, choices=UserStatus.choices, default=UserStatus.TEACHER)
    profile_image = models.ImageField(default='profile-pictures/user-default.png', upload_to='profile-images/',
                                      blank=True)
    is_teacher = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['email']
        permissions = (
            ('can_view_teacher_dashboard', 'Can view Teacher Dashboard'),
            ('can_view_admin_dashboard', 'Can view Admin Dashboard'),
            ('can_view_superuser_dashboard', 'Can view Superuser Dashboard'),
        )


class Teacher(User):
    """
    Proxy model representing a teacher user.
    """
    objects = TeacherManager()

    class Meta:
        proxy = True
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'

    def save(self, *args, **kwargs):
        """
        Overrides save method to set is_teacher=True and other role fields appropriately.
        """
        self.is_teacher = True
        self.is_admin = False
        self.is_superuser = False
        self.is_student = False
        self.status = UserStatus.TEACHER
        super().save(*args, **kwargs)


class Admin(User):
    """
    Proxy model representing an admin user.
    """
    objects = AdminManager()

    class Meta:
        proxy = True
        verbose_name = 'Admin'
        verbose_name_plural = 'Admins'

    def save(self, *args, **kwargs):
        """
        Overrides save method to set is_admin=True and other role fields appropriately.
        """
        self.is_teacher = False
        self.is_admin = True
        self.is_superuser = False
        self.is_student = False
        self.status = UserStatus.ADMIN
        super().save(*args, **kwargs)


class SuperAdmin(User):
    """
    Proxy model representing a super admin user.
    """
    objects = SuperAdminManager()

    class Meta:
        proxy = True
        verbose_name = 'Super Admin'
        verbose_name_plural = 'Super Admins'

    def save(self, *args, **kwargs):
        """
        Overrides save method to set is_superuser=True and other role fields appropriately.
        """
        self.is_teacher = False
        self.is_admin = False
        self.is_superuser = True
        self.is_student = False
        self.status = UserStatus.SUPERUSER
        super().save(*args, **kwargs)


class Student(User):
    """
    Proxy model representing a student user.
    """
    objects = StudentManager()

    class Meta:
        proxy = True
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def save(self, *args, **kwargs):
        """
        Overrides save method to set is_student=True and other role fields appropriately.
        """
        self.is_teacher = False
        self.is_admin = False
        self.is_superuser = False
        self.is_student = True
        self.status = UserStatus.STUDENT
        super().save(*args, **kwargs)
