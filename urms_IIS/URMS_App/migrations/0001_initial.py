# Generated by Django 5.1.7 on 2025-04-23 16:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32)),
                ('email', models.CharField(max_length=254)),
                ('isActive', models.BooleanField()),
                ('password', models.CharField(editable=False, max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=127)),
                ('album', models.CharField(max_length=127)),
                ('releaseDate', models.DateField()),
                ('dateAdded', models.DateField()),
                ('currentRating', models.DecimalField(decimal_places=1, max_digits=2)),
                ('totalVotes', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TestModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('string', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='UploadedImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='uploads/')),
            ],
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='URMS_App.user')),
            ],
            bases=('URMS_App.user',),
        ),
    ]
