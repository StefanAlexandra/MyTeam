# Generated by Django 4.2.3 on 2023-09-02 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userextend', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(max_length=10),
        ),
    ]