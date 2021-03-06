# Generated by Django 2.2 on 2019-12-18 04:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sales', '0005_auto_20191216_2224'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user_updated', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=100)),
                ('duration', models.TimeField()),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('img', models.ImageField(blank=True, null=True, upload_to='videos')),
                ('video', models.FileField(blank=True, null=True, upload_to='videos')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.Contract')),
                ('user_created', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
