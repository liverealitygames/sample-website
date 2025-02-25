# Generated by Django 5.1.6 on 2025-02-25 04:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('community', '0001_initial'),
        ('homepage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('banner', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='homepage.externalimage')),
                ('season', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='community.season')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
