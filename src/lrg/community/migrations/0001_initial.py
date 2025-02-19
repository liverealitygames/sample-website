# Generated by Django 5.1.6 on 2025-02-19 00:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('homepage', '0001_initial'),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('wiki', models.CharField(blank=True, null=True)),
                ('instagram', models.CharField(blank=True, null=True)),
                ('facebook', models.CharField(blank=True, null=True)),
                ('bluesky', models.CharField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('game_length_range_shortest', models.IntegerField(blank=True, null=True)),
                ('game_length_range_longest', models.IntegerField(blank=True, null=True)),
                ('game_length_range_exact', models.IntegerField(blank=True, null=True)),
                ('start_time_range_earliest', models.DateField(blank=True, null=True)),
                ('start_time_range_latest', models.DateField(blank=True, null=True)),
                ('start_time_specific', models.DateField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Casting', 'Casting'), ('Running', 'Running'), ('Hiatus', 'Hiatus'), ('Defunct', 'Defunct'), ('Unknown', 'Unknown'), ('Under Review', 'Under Review')])),
                ('banner', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='homepage.externalimage')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='communities_owned', to='profiles.profile')),
                ('staff', models.ManyToManyField(related_name='communities_as_staff', to='profiles.profile')),
                ('contact', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='community.contactinfo')),
            ],
            options={
                'verbose_name_plural': 'communities',
            },
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, null=True)),
                ('number', models.IntegerField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Casting', 'Casting'), ('Running', 'Running'), ('Finished', 'Finished'), ('Under Review', 'Under Review')])),
                ('filmed', models.BooleanField(blank=True, null=True)),
                ('application_link', models.CharField(blank=True, null=True)),
                ('format', models.CharField(choices=[('Amazing Race', 'Amazing Race'), ('Big Brother', 'Big Brother'), ('Survivor', 'Survivor'), ('The Challenge', 'The Challenge'), ('The Mole', 'The Mole'), ('Traitors', 'Traitors'), ('Taskmaster', 'Taskmaster')])),
                ('banner', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='homepage.externalimage')),
                ('cast', models.ManyToManyField(related_name='seasons_as_cast', to='profiles.profile')),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='community.community')),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='homepage.location')),
                ('schedule', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='community.schedule')),
                ('staff', models.ManyToManyField(related_name='seasons_as_staff', to='profiles.profile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
