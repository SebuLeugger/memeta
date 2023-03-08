# Generated by Django 4.1.6 on 2023-02-20 13:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('memeta_app', '0020_rename_subject_card_course_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='memeta_app.event'),
        ),
        migrations.AlterField(
            model_name='card',
            name='appreciated_by',
            field=models.ManyToManyField(blank=True, related_name='appreciated_cards', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='card',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='memeta_app.course'),
        ),
        migrations.AlterField(
            model_name='card',
            name='sorted_out_by',
            field=models.ManyToManyField(blank=True, related_name='sorted_out_cards', to=settings.AUTH_USER_MODEL),
        ),
    ]