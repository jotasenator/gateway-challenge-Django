from django.db import models

from django.core.validators import MinValueValidator


# Create your models here.
class Gateway(models.Model):
    serial_number = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=200)
    ipv4_address = models.GenericIPAddressField(protocol="IPv4")


class PeripheralDevice(models.Model):
    uid = models.IntegerField(unique=True, validators=[MinValueValidator(0)])
    vendor = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=200, choices=[("online", "Online"), ("offline", "Offline")]
    )
    gateway = models.ForeignKey(
        Gateway, on_delete=models.CASCADE, related_name="peripheral_devices"
    )
