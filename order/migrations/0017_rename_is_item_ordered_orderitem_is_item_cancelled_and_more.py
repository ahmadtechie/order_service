# Generated by Django 4.2.6 on 2024-01-13 02:51

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0016_alter_order_delivery_charge_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="orderitem",
            old_name="is_item_ordered",
            new_name="is_item_cancelled",
        ),
        migrations.RemoveField(
            model_name="ordercancellation",
            name="is_order_cancelled",
        ),
        migrations.AddField(
            model_name="order",
            name="is_order_cancelled",
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name="OrderItemCancellation",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("order_item_cancel_reason", models.TextField()),
                (
                    "order_item",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="order_item_cancels",
                        to="order.orderitem",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
