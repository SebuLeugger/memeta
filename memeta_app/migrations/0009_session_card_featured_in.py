# Generated by Django 4.1.6 on 2023-02-16 13:55

from django.conf import settings
from django.db import migrations, models
import memeta_app.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('memeta_app', '0008_rename_exluded_by_card_excluded_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(auto_now_add=True)),
                ('student', models.ForeignKey(on_delete=models.SET(memeta_app.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='card',
            name='featured_in',
            field=models.ManyToManyField(related_name='featured_cards', to='memeta_app.session'),
        ),
    ]