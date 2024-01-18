from django.db import models
from django.contrib.auth.tokens import default_token_generator
from person.models import User
import secrets

class Chat(models.Model):
    name = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    time_create = models.TimeField(auto_now=True)
    ref_token = models.TextField()

    def __str__(self):
        return self.name

    def save(self,  *args, **kwargs):
        self.ref_token = secrets.token_hex(16)
        super(Chat, self).save(*args, **kwargs)



class Person_Chat(models.Model):
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

