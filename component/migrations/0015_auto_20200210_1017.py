# Generated by Django 2.2.7 on 2020-02-10 14:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('component', '0014_subproduct_place'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subproduct',
            old_name='medidas',
            new_name='measure',
        ),
    ]