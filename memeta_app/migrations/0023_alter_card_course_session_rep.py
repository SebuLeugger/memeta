# Generated by Django 4.1.6 on 2023-02-21 12:06

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('memeta_app', '0022_remove_card_event_alter_card_course_delete_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='memeta_app.course'),
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('sequence', models.CharField(max_length=255, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')])),
                ('cards', models.ManyToManyField(related_name='featured_in', to='memeta_app.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='memeta_app.card')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='memeta_app.session')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]