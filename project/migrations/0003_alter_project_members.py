# Generated by Django 4.2.3 on 2023-08-01 06:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='members',
            field=models.ManyToManyField(limit_choices_to={'is_staff': False}, to=settings.AUTH_USER_MODEL),
        ),
    ]