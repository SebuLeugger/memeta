# Generated by Django 4.1.6 on 2023-02-16 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('memeta_app', '0007_card_exluded_by'),
    ]

    operations = [
        migrations.RenameField(
            model_name='card',
            old_name='exluded_by',
            new_name='excluded_by',
        ),
    ]
