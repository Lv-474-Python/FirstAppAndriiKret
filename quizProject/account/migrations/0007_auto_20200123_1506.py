# Generated by Django 3.0.2 on 2020-01-23 15:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20200123_1420'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='admin',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='staff',
        ),
    ]
