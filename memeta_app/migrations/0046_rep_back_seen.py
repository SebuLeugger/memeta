# Generated by Django 4.1.6 on 2023-03-02 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memeta_app', '0045_remove_rep_card_correct_remove_rep_i_understand_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='rep',
            name='back_seen',
            field=models.BooleanField(default=False),
        ),
    ]
