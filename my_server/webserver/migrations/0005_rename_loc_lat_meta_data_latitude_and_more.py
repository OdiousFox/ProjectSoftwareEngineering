# Generated by Django 4.1.3 on 2022-12-17 20:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webserver', '0004_remove_meta_data_loc_alt'),
    ]

    operations = [
        migrations.RenameField(
            model_name='meta_data',
            old_name='loc_lat',
            new_name='latitude',
        ),
        migrations.RenameField(
            model_name='meta_data',
            old_name='loc_lon',
            new_name='longitude',
        ),
    ]