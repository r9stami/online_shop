# Generated by Django 5.0.7 on 2024-08-05 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_discountcode_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.TextField(default='kos'),
        ),
    ]
