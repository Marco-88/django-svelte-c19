from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.formats import localize

from posts.models import Post


# class Message(models.Model):
#
#     body = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#
#     class Meta:
#         ordering = ['-updated_at', 'updated_at', '-created_at', 'created_at', 'user', '-user']
#
#     def __str__(self):
#         return self.user.username + 's message from ' + localize(self.created_at)
#
#
# class Chat(models.Model):
#
#     title = models.CharField(max_length=100)
#     users = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=[])
#     messages = models.ForeignKey(Message, on_delete=models.CASCADE, default=[])
#
#     def __str__(self):
#         return self.title
