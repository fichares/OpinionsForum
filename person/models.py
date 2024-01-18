import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser




class User(AbstractUser):
    photo = models.ImageField(default='photo_default_user.png')
    adress = models.TextField(max_length=80, default='')
    location = models.TextField(default='')
    privilege = models.BooleanField(default='False')
    slug_url = models.TextField(max_length=40, unique=True)
    last_ip_adress = models.TextField(max_length=40, default='')




class Notes(models.Model):
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.TextField(max_length=50)
    time_create = models.TimeField(auto_now=True)
    time_publicate = models.TimeField()
    text = models.TextField()

class Files(models.Model):
    uuid = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
    name = models.CharField()
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    time_create = models.TimeField(auto_now=True)
    files = models.FileField(upload_to='person/files/% Y/% m/% d/', null=True, blank=True)

    def __str__(self):
        return self.name



