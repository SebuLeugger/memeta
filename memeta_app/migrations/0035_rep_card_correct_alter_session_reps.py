# Generated by Django 4.1.6 on 2023-02-25 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memeta_app', '0034_session_reps'),
    ]

    operations = [
        migrations.AddField(
            model_name='rep',
            name='card_correct',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='reps',
            field=models.ManyToManyField(blank=True, to='memeta_app.rep'),
        ),
    ]
