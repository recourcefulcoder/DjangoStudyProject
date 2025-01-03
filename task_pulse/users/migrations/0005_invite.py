# Generated by Django 4.2.6 on 2023-12-18 13:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('workplace', '0004_rename_manager_task_author'),
        ('users', '0004_alter_user_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invite',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'expire_datetime',
                    models.DateTimeField(
                        default=None, null=True, verbose_name='expire_datetime'
                    ),
                ),
                (
                    'company',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='workplace.company',
                        verbose_name='company',
                    ),
                ),
                (
                    'invited_user',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name='invited_user',
                    ),
                ),
            ],
        ),
    ]
