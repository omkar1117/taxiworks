from django.db import models
from user.models import User

# Create your models here.


class Rydes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

