# Generated by Django 4.2.4 on 2023-10-19 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0003_alter_customuser_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('Customer', 'customer'), ('Restaurent Owner', 'owner')], max_length=20),
        ),
    ]
