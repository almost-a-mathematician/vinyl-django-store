# Generated by Django 4.1.5 on 2023-01-18 18:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_order_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
    ]