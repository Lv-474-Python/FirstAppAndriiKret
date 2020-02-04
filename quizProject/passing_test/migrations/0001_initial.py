# Generated by Django 3.0.2 on 2020-02-04 14:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('test_app', '0007_auto_20200204_1330'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAnswers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chosen_answer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='test_app.AnswerOption')),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='test_app.Questions')),
                ('test', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='test_app.TestQuiz')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
