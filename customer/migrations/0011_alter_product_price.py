# Generated by Django 4.2.3 on 2023-07-28 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0010_alter_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.IntegerField(),
        ),
    ]
