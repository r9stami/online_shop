# Generated by Django 5.0.7 on 2024-08-02 07:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_alter_like_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='product',
        ),
        migrations.RemoveField(
            model_name='like',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='like',
            name='user',
        ),
    ]
