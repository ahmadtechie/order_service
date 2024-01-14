# Generated by Django 4.2.5 on 2023-09-22 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_alter_orderitem_variation_ids'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['order_total_price']},
        ),
        migrations.AlterModelOptions(
            name='orderitem',
            options={'ordering': ['item_price']},
        ),
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Cancelled', 'Cancelled'), ('Delivered', 'Delivered')], default='Pending', max_length=15),
        ),
    ]