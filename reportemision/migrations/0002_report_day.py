# Generated by Django 2.2 on 2020-08-06 04:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0006_contract_auspice'),
        ('content', '0008_auto_20200707_1824'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reportemision', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report_day',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user_updated', models.IntegerField(blank=True, null=True)),
                ('date_now', models.DateField()),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.Contract')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.Order')),
                ('playlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.Playlist')),
                ('user_created', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.Video')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
