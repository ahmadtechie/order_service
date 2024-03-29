# Generated by Django 4.1.7 on 2023-09-20 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_order_is_order_cancelled'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='product_price',
            new_name='item_price',
        ),
        migrations.AddField(
            model_name='order',
            name='order_total',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8),
        ),
    ]
