from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class BaseClass(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    mobile = models.CharField(max_length=11, null=True, blank=True)
    is_provider = models.BooleanField(default=False)
    is_rider = models.BooleanField(default=False)
    avatar = models.FileField(upload_to='avatars/', null=True, blank=True)


class Otp(BaseClass):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    is_expired = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


class Address(BaseClass):
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)

    def __str__(self):
        return "%s-%s" % (self.address, self.state)


class UserAddress(BaseClass):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ManyToManyField(Address)

    def __str__(self):
        return self.user.username