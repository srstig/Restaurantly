# Generated by Django 5.1.7 on 2025-03-21 07:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cafeapp', '0004_alter_booking_number'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Transaction',
        ),
    ]
