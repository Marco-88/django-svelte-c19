from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from multiselectfield import MultiSelectField
from djangraph.constants import GENRES


class UserGroup(models.Model):
    name = models.TextField(default='', max_length=2048, unique=True)
    description = models.TextField(default='', max_length=2048)
    image = models.ImageField(default='default_group.jpg', upload_to='group_pics', null=True)
    genres = MultiSelectField(choices=GENRES, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_groups')
    users = models.ManyToManyField(User, default=[], related_name='member_groups')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at', '-created_at', 'updated_at', '-updated_at', 'name', '-name', 'owner', '-owner']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('group', kwargs={'name': self.name})
