# Generated by Django 3.0.2 on 2020-03-21 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('votes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentvote',
            name='vote',
            field=models.CharField(choices=[('NONE', 'NONE'), ('UP', 'UP'), ('DOWN', 'DOWN')], default='NONE', max_length=20),
        ),
        migrations.AlterField(
            model_name='postvote',
            name='vote',
            field=models.CharField(choices=[('NONE', 'NONE'), ('UP', 'UP'), ('DOWN', 'DOWN')], default='NONE', max_length=20),
        ),
    ]
