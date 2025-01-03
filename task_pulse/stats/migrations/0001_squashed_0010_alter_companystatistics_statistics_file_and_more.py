# Generated by Django 4.2.6 on 2023-12-21 16:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    replaces = [
        ('stats', '0001_initial'),
        ('stats', '0002_alter_companyuserstatistics_statistics_file'),
        ('stats', '0003_alter_companyuserstatistics_statistics_file'),
        ('stats', '0004_alter_companyuserstatistics_user'),
        ('stats', '0005_alter_companyuserstatistics_statistics_file'),
        ('stats', '0006_alter_companyuserstatistics_user'),
        ('stats', '0007_companyuserstatistics_company'),
        ('stats', '0008_remove_companyuserstatistics_company'),
        ('stats', '0009_alter_companyuserstatistics_include_tasks_and_more'),
        ('stats', '0010_alter_companystatistics_statistics_file_and_more'),
    ]

    initial = True

    dependencies = [
        ('workplace', '0008_alter_task_status_and_more'),
        ('workplace', '0006_task_status_taskstatuschangelog'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyStatistics',
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
                    'include_users',
                    models.BooleanField(
                        help_text='Does report include user statistics in this company?',
                        verbose_name='include users',
                    ),
                ),
                (
                    'include_tasks',
                    models.BooleanField(
                        help_text='Does report include user tasks?',
                        verbose_name='include tasks',
                    ),
                ),
                (
                    'statistics_file',
                    models.FileField(
                        help_text='Path to file with company statistics',
                        upload_to='statistics/company',
                        verbose_name='company statistics file',
                    ),
                ),
                (
                    'date_from',
                    models.DateField(
                        help_text='Start date company statistics',
                        verbose_name='statistics from: (date)',
                    ),
                ),
                (
                    'date_to',
                    models.DateField(
                        help_text='End date company statistics',
                        verbose_name='statistics to: (date)',
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text='Date of creation company statistics report',
                        verbose_name='date of creation',
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
            ],
        ),
        migrations.CreateModel(
            name='CompanyUserStatistics',
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
                    'include_tasks',
                    models.BooleanField(
                        help_text='Does report include tasks?',
                        verbose_name='include tasks',
                    ),
                ),
                (
                    'statistics_file',
                    models.FileField(
                        help_text='Path to file with user statistics',
                        upload_to='statistics/users',
                        verbose_name='user statistics file',
                    ),
                ),
                (
                    'date_from',
                    models.DateField(
                        help_text='Start date user statistics',
                        verbose_name='statistics from: (date)',
                    ),
                ),
                (
                    'date_to',
                    models.DateField(
                        help_text='End date user statistics',
                        verbose_name='statistics to: (date)',
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text='Date of creation user statistics report',
                        verbose_name='date of creation',
                    ),
                ),
                (
                    'user',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='workplace.companyuser',
                        verbose_name='user',
                    ),
                ),
            ],
        ),
    ]
