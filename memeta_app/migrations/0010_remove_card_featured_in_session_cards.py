# Generated by Django 4.1.6 on 2023-02-16 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memeta_app', '0009_session_card_featured_in'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='featured_in',
        ),
        migrations.AddField(
            model_name='session',
            name='cards',
            field=models.ManyToManyField(related_name='featured_in', to='memeta_app.card'),
        ),
    ]
