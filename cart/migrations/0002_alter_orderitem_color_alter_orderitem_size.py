# Generated by Django 5.0.7 on 2024-07-31 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='color',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='size',
            field=models.CharField(max_length=60),
        ),
    ]
