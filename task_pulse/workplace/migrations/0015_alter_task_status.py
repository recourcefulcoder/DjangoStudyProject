# Generated by Django 4.2.6 on 2023-12-23 13:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            'workplace',
            '0014_alter_companyuser_company_alter_companyuser_user_and_more',
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(
                choices=[
                    ('given', 'Выданные'),
                    ('active', 'Активная задача'),
                    ('postponed', 'Отложенные'),
                    ('review', 'На проверке'),
                    ('rejected', 'На доработке'),
                    ('completed', 'Завершённые'),
                ],
                default='given',
                help_text='Task current status',
                max_length=20,
                verbose_name='status',
            ),
        ),
    ]
