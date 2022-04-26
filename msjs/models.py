# from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models

class Message(models.Model):
    """Model definition for message."""

    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    text = models.TextField()
    location = models.PointField(null=True, blank=True)
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
