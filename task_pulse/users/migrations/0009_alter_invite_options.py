# Generated by Django 4.2.6 on 2023-12-22 10:54

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0008_invite_assigned_role'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='invite',
            options={
                'verbose_name': 'invite',
                'verbose_name_plural': 'invites',
            },
        ),
    ]
