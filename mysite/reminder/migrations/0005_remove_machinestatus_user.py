# Generated by Django 2.2.28 on 2022-12-09 06:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reminder', '0004_machinestatus_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='machinestatus',
            name='user',
        ),
    ]
