from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group
from .managers import CustomUserManager

# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    MONTH_CHOICES = [
        (1, 'January'),
        (2, 'February'),
        (3, 'March'),
        (4, 'April'),
        (5, 'May'),
        (6, 'June'),
        (7, 'July'),
        (8, 'August'),
        (9, 'September'),
        (10, 'October'),
        (11, 'November'),
        (12, 'December'),
    ]

    username = None
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    birth_day = models.PositiveIntegerField(null=True)
    birth_month = models.PositiveIntegerField(choices=MONTH_CHOICES, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    role = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)

    USERNAME_FIELD = "email"

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.role:
            self.groups.set([self.role])
        else:
            self.groups.clear()
