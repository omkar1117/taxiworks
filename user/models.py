from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    mobile = models.CharField(max_length=11, null=True, blank=True)
    is_provider = models.BooleanField(default=False)
    is_rider = models.BooleanField(default=False)
    avatar = models.FileField(upload_to='avatars/', null=True, blank=True)


class Otp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    is_expired = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
