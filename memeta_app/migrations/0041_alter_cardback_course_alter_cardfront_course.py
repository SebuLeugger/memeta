# Generated by Django 4.1.6 on 2023-03-01 15:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('memeta_app', '0040_alter_card_appreciated_by_alter_card_sorted_out_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardback',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='memeta_app.course'),
        ),
        migrations.AlterField(
            model_name='cardfront',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='memeta_app.course'),
        ),
    ]
