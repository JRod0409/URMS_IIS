# Generated by Django 5.1.2 on 2025-04-29 02:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('URMS_App', '0006_song_spotify_url_alter_song_album_art_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField()),
                ('rated_at', models.DateTimeField(auto_now_add=True)),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='URMS_App.song')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='URMS_App.user')),
            ],
        ),
    ]
