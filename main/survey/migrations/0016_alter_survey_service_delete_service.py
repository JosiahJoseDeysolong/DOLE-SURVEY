# Generated by Django 5.1.1 on 2024-09-20 03:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0005_service'),
        ('survey', '0015_service_alter_survey_service'),
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
