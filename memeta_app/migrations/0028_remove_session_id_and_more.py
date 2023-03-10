# Generated by Django 4.1.6 on 2023-02-23 20:45

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    dependencies = [
        ('memeta_app', '0027_remove_session_reps_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='id',
        ),
        migrations.RemoveField(
            model_name='session',
            name='string_of_list_of_card_pks',
        ),
        migrations.AddField(
            model_name='session',
            name='card_pk_list_string',
            field=models.TextField(blank=True, default='', null=True, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')]),
        ),
        migrations.AddField(
            model_name='session',
            name='preferences',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='memeta_app.preferences'),
        ),
    ]
