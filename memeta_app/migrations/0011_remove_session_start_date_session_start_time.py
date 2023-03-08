# Generated by Django 4.1.6 on 2023-02-16 14:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('memeta_app', '0010_remove_card_featured_in_session_cards'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='start_date',
        ),
        migrations.AddField(
            model_name='session',
            name='start_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
