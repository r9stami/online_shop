# Generated by Django 5.0.7 on 2024-08-01 09:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_size_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='size',
            name='category',
        ),
    ]