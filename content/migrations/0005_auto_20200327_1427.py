# Generated by Django 2.2 on 2020-03-27 18:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0004_auto_20200327_1237'),
    ]

    operations = [
        migrations.RenameField(
            model_name='playlist_spot_detail',
            old_name='repeticiones',
            new_name='repeat_count',
        ),
    ]
