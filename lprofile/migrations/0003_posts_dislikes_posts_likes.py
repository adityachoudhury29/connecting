# Generated by Django 4.1.6 on 2023-04-30 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lprofile', '0002_alter_posts_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='dislikes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='posts',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]