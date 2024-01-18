from django.db import models

from chat.models import Chat
from person.models import User


class Publication(models.Model):
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    chats = models.ForeignKey(Chat, on_delete=models.CASCADE)
    time_send = models.DateTimeField(auto_now=True)
    text = models.TextField()
