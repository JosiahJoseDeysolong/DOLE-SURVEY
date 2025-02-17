# Generated by Django 5.1.1 on 2024-09-18 03:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0011_rename_services_service'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='division',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.division'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='contact_number',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='survey',
            name='division',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.division'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='survey',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='survey',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.service'),
        ),
    ]
