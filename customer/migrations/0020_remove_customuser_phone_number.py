# Generated by Django 4.2.3 on 2023-08-04 04:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0019_remove_customuser_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='phone_number',
        ),
    ]
