from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from multiselectfield import MultiSelectField

# from chat.models import Chat
from djangraph.constants import GENRES


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default_user.jpg', upload_to='profile_pics', null=True)
    description = models.TextField(default='', max_length=2048)
    genres = MultiSelectField(choices=GENRES, null=True)
    dark = models.BooleanField(default=True)
    birthdate = models.DateField(null=True)
    friends = models.ManyToManyField(User, default=[], related_name='friends')
    # chats = models.ForeignKey(Chat, on_delete=models.CASCADE, default=[])

    def __str__(self):
        return f'{self.user.username} Profile'

    def get_absolute_url(self):
        return reverse('profile', kwargs={'username': self.user.username})
