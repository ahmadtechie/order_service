# Generated by Django 4.1.7 on 2023-09-20 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_rename_order_total_order_order_total_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='address',
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_address_id',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Address',
        ),
    ]
