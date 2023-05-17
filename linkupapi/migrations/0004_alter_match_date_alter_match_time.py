# Generated by Django 4.2.1 on 2023-05-17 20:09

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('linkupapi', '0003_alter_match_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='match',
            name='time',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
    ]
