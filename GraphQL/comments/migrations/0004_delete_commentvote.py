# Generated by Django 3.0.2 on 2020-03-20 17:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0003_commentvote'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CommentVote',
        ),
    ]