from django.db import models
from django.contrib.auth.models import User



class UserInfo(models.Model):

    objects: models.query.QuerySet

    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    avatar = models.FileField(upload_to='avatar/', null=True)
    avatarBinary = models.BinaryField(null=True)
    

