# Generated by Django 5.0.1 on 2024-01-30 08:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hotel',
            name='total_rooms',
        ),
    ]
