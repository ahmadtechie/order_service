# Generated by Django 4.1.7 on 2023-09-20 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_order_cancelled',
            field=models.BooleanField(default=False),
        ),
    ]
