# from django.db import models
from tabnanny import verbose
from django.contrib.auth.models import User
from django.contrib.gis.db import models

class Message(models.Model):
    """Model definition for message."""

    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    text = models.TextField()
    location = models.PointField(default="POINT(1,1)")
    addres = models.CharField(max_length=100, null=True, blank=True)
    added = models.DateTimeField(auto_now_add=True)
    banned = models.BooleanField(default=False)
    active = models.BooleanField(default=True)


    class Meta:
        """Meta definition for message."""

        verbose_name = 'message'
        verbose_name_plural = 'messages'

    def __str__(self):
        """Unicode representation of message."""
        return str(self.owner.username)

    def get_likes(self):
        return MessageLike.objects.filter(message=self).count()

class MessageLike(models.Model):
    message = models.ForeignKey(Message, on_delete=models.PROTECT)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Message Like'
        verbose_name_plural = 'Message Likes'

    def __str__(self):
        return str(self.owner.username + ' - ' + self.message.id)