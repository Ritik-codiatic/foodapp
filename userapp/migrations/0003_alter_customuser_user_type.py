# Generated by Django 4.2.4 on 2023-10-19 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0002_rename_gender_types_customuser_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('customer', 'Customer'), ('owner', 'Restaurent Owner')], max_length=20),
        ),
    ]
