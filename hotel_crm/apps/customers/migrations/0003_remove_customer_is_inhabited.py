# Generated by Django 5.0.1 on 2024-04-08 14:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_rename_status_customer_is_inhabited'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='is_inhabited',
        ),
    ]