# Generated by Django 2.2 on 2020-03-27 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0005_auto_20200327_1427'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist_client_detail',
            name='time_total',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
