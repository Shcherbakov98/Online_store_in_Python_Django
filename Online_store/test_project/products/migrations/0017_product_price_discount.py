# Generated by Django 3.0.4 on 2020-04-03 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_remove_product_price_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price_discount',
            field=models.IntegerField(default=0),
        ),
    ]
