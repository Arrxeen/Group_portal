from django.db import models
from auth_sys.models import CustomUser

# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="authored_news"
    )
    editor = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="edited_news",
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        permissions = [('can_post_news', 'Can post news')]

    def __str__(self):
        return self.title
    
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()

    class Meta:
        permissions = [('can_modify_event', 'Can modify events')]

    def __str__(self):
        return f"{self.title} ({self.date})"

class Notification(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = [('can_create_notification', 'Can create notification'),
                       ('can_modify_notification', 'Can modify notification')]

    def __str__(self):
        return self.title

class UsefulLink(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [
            ('can_add_useful_link', 'Can add useful link'),
            ('can_edit_useful_link', 'Can edit useful link'),
            ('can_delete_useful_link', 'Can delete useful link')
        ]

    def __str__(self):
        return self.title   