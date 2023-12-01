# Generated by Django 4.2.3 on 2023-07-26 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_customuser_is_email_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='username',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
