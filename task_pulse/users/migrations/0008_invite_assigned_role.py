# Generated by Django 4.2.6 on 2023-12-21 13:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0007_remove_invite_invited_user_invite_invited_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='invite',
            name='assigned_role',
            field=models.CharField(
                choices=[('manager', 'Manager'), ('employee', 'Employee')],
                default=('manager', 'Manager'),
                help_text='Role for company user',
                max_length=20,
                verbose_name='role',
            ),
        ),
    ]
