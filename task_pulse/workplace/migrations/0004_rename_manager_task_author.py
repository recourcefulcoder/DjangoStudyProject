# Generated by Django 4.2.6 on 2023-12-13 18:16

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('workplace', '0003_alter_companyuser_user_task'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='manager',
            new_name='author',
        ),
    ]