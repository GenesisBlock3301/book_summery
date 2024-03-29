# Generated by Django 4.1.7 on 2023-02-23 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=100, null=True)),
                ('email', models.EmailField(max_length=255, null=True, unique=True)),
                ('password', models.CharField(max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('auth_provider', models.CharField(blank=True, default='self', max_length=100)),
            ],
            options={
                'index_together': {('username', 'email')},
            },
        ),
    ]
