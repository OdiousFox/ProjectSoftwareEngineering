# Generated by Django 4.1.3 on 2022-12-20 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webserver', '0006_py_averages_humidity_pyentries_humidity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='py_averages',
            name='light',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='pyentries',
            name='light',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
    ]
