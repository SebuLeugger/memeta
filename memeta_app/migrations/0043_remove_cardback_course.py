# Generated by Django 4.1.6 on 2023-03-01 16:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('memeta_app', '0042_alter_cardback_course_alter_cardfront_course'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cardback',
            name='course',
        ),
    ]
