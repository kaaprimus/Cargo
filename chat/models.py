from django.db import models
from django.conf import settings

class Rooms(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

class Messages(models.Model):
    room = models.ForeignKey(Rooms, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_added',)
