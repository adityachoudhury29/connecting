# Generated by Django 4.1.6 on 2023-05-05 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lprofile', '0016_alter_profile1_connection'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile1',
            name='firstname',
        ),
        migrations.RemoveField(
            model_name='profile1',
            name='lastname',
        ),
        migrations.AlterField(
            model_name='profile1',
            name='about',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]