# Generated by Django 2.2.28 on 2022-12-05 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reminder', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machinestatus',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
