from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.formats import localize

from posts.models import Post


class Comment(models.Model):

    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, related_name='comment_comments', null=True, blank=True)
    parent_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments', null=True, blank=True)

    class Meta:
        ordering = ['-updated_at', 'updated_at', '-created_at', 'created_at', 'user', '-user']

    def __str__(self):
        return self.user.username + 's comment from ' + localize(self.created_at)
