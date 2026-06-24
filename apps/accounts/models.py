from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Editor', 'Editor'),
        ('Viewer', 'Viewer'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Viewer')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'accounts_user'

class Preference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    theme = models.CharField(max_length=10, default='light')
    grid_page_size = models.IntegerField(default=50)
    email_notifications = models.BooleanField(default=True)

    class Meta:
        db_table = 'accounts_preference'
