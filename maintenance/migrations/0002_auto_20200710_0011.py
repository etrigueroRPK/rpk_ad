# Generated by Django 2.2 on 2020-07-10 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maintenance',
            name='created_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
