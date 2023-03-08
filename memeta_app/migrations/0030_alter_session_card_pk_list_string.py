# Generated by Django 4.1.6 on 2023-02-23 21:08

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('memeta_app', '0029_alter_session_preferences'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='card_pk_list_string',
            field=models.TextField(validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')]),
        ),
    ]
