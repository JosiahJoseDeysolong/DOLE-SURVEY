# Generated by Django 5.1.1 on 2024-09-18 01:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0010_services_alter_survey_service'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Services',
            new_name='Service',
        ),
    ]
