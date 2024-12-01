from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group
from .managers import CustomUserManager

# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):

    # ROLE = [
    #     ('Student', 'student'),
    #     ('Moderator','moderator'),
    #     ('Administrator','administrator')
    # ]

    username = None
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    # role = models.CharField(max_length=13, choices=ROLE, default='student')
    role = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
        
    USERNAME_FIELD = "email"

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
