# Generated by Django 4.2.6 on 2023-12-16 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('workplace', '0005_task_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.CharField(
                choices=[
                    ('in_process', 'In Process'),
                    ('complete', 'Complete'),
                    ('on_checking', 'On Checking'),
                    ('rejected', 'Rejected'),
                ],
                default='in_process',
                help_text='current task status',
                max_length=20,
                verbose_name='task status',
            ),
        ),
        migrations.CreateModel(
            name='TaskStatusChangeLog',
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
                    'from_status',
                    models.CharField(
                        choices=[
                            ('in_process', 'In Process'),
                            ('complete', 'Complete'),
                            ('on_checking', 'On Checking'),
                            ('rejected', 'Rejected'),
                        ],
                        help_text='changed from: (task status)',
                        max_length=20,
                        verbose_name='from status',
                    ),
                ),
                (
                    'to_status',
                    models.CharField(
                        choices=[
                            ('in_process', 'In Process'),
                            ('complete', 'Complete'),
                            ('on_checking', 'On Checking'),
                            ('rejected', 'Rejected'),
                        ],
                        help_text='changed to: (task status)',
                        max_length=20,
                        verbose_name='to status',
                    ),
                ),
                (
                    'changed_at',
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text='status change date',
                        verbose_name='change date',
                    ),
                ),
                (
                    'task',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='status_changes',
                        to='workplace.task',
                        verbose_name='task object',
                    ),
                ),
            ],
        ),
    ]
