from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from user_groups.models import UserGroup


class Post(models.Model):

    title = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    group = models.ForeignKey(UserGroup, null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-updated_at', 'updated_at', '-created_at', 'created_at', 'group', '-group', 'user', '-user', 'title', '-title']

    def __str__(self):
        return self.title
