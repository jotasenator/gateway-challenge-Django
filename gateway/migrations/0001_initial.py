# Generated by Django 4.2.2 on 2023-07-11 18:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gateway',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.CharField(max_length=200, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('ipv4_address', models.GenericIPAddressField(protocol='IPv4')),
            ],
        ),
        migrations.CreateModel(
            name='PeripheralDevice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.IntegerField(unique=True)),
                ('vendor', models.CharField(max_length=200)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('online', 'Online'), ('offline', 'Offline')], max_length=200)),
                ('gateway', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='peripheral_devices', to='gateway.gateway')),
            ],
        ),
    ]
