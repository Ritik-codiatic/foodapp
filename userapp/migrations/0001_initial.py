# Generated by Django 4.2.4 on 2023-10-09 05:34

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import userapp.custommanager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userapp.state')),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_type', models.CharField(choices=[('Customer', 'customer'), ('Restaurent Owner', 'owner')], max_length=20)),
                ('mobile_number', models.CharField(error_messages={'unique': 'A user is already registered with this Mobile number'}, max_length=10, null=True, unique=True)),
                ('address', models.TextField(max_length=100)),
                ('gender_types', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=20)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='pics')),
                ('email', models.EmailField(error_messages={'unique': 'A user is already registered with this email address'}, max_length=254, unique=True, verbose_name='email address')),
                ('city_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='userapp.city')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', userapp.custommanager.UserManager()),
            ],
        ),
    ]
