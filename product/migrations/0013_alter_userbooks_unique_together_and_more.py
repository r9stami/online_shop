# Generated by Django 5.0.7 on 2024-08-04 07:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0012_remove_comment_name_remove_comment_phone_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userbooks',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='userbooks',
            name='user_id',
        ),
        migrations.DeleteModel(
            name='FavBooks',
        ),
        migrations.DeleteModel(
            name='UserBooks',
        ),
    ]
