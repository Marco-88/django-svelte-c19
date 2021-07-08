from django.db import models
from django.conf import settings

VOTES = [
    ('NONE', 'NONE'),
    ('UP', 'UP'),
    ('DOWN', 'DOWN')
]


class PostVote(models.Model):
    vote = models.CharField(
        max_length = 20,
        choices = VOTES,
        default = 'NONE'
        )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey('posts.Post', related_name='votes', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')


class CommentVote(models.Model):
    vote = models.CharField(
        max_length=20,
        choices=VOTES,
        default='NONE'
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.ForeignKey('comments.Comment', related_name='votes', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'comment')
