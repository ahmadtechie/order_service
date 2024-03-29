# Generated by Django 4.1.7 on 2023-09-20 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_remove_order_address_order_delivery_address_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='is_order_cancelled',
            new_name='cancel_order',
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_charge',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
    ]
