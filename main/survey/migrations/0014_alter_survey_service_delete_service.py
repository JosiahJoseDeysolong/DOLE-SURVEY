# Generated by Django 5.1.1 on 2024-09-20 02:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0002_service'),
        ('survey', '0013_remove_survey_division_remove_service_division_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='office.service'),
        ),
        migrations.DeleteModel(
            name='Service',
        ),
    ]
