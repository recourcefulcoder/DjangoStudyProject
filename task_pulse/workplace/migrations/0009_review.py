# Generated by Django 4.2.6 on 2023-12-21 19:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('workplace', '0008_task_review_responsible'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
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
                ('message', models.TextField(verbose_name='review_message')),
                (
                    'task',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='review',
                        to='workplace.task',
                        verbose_name='task',
                    ),
                ),
            ],
        ),
    ]
