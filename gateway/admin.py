from django.contrib import admin
from .models import Gateway, PeripheralDevice


# Register your models here.
admin.site.register(Gateway)
admin.site.register(PeripheralDevice)
