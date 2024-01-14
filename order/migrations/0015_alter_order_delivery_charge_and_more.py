# Generated by Django 4.2.6 on 2024-01-10 13:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0014_alter_order_order_total_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="delivery_charge",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="item_price",
            field=models.FloatField(blank=True, null=True),
        ),
    ]
