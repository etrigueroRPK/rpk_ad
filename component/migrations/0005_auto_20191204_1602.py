# Generated by Django 2.2.7 on 2019-12-04 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('component', '0004_auto_20191204_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='img',
            field=models.ImageField(null=True, upload_to='categories'),
        ),
    ]
