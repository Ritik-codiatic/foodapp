# Generated by Django 4.2.4 on 2023-10-31 09:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('restaurantapp', '0016_alter_orderdetail_amount_restaurantrating'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
