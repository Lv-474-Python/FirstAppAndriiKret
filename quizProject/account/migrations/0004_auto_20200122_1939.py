# Generated by Django 3.0.2 on 2020-01-22 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_login_reg', '0003_auto_20200122_1931'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default=1234, max_length=128, verbose_name='password'),
            preserve_default=False,
        ),
    ]
