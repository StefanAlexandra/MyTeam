# Generated by Django 4.2.4 on 2024-02-04 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userextend', '0002_alter_user_first_name_alter_user_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='country',
            field=models.CharField(max_length=50),
        ),
    ]
