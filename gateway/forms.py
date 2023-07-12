from django import forms
from .models import Gateway, PeripheralDevice

from django.forms import ModelChoiceField

import ipaddress


class GatewayForm(forms.ModelForm):
    class Meta:
        model = Gateway
        fields = ["name", "serial_number", "ipv4_address"]

    def clean_ipv4_address(self):
        ipv4_address = self.cleaned_data.get("ipv4_address")
        try:
            ipaddress.IPv4Address(ipv4_address)
        except ipaddress.AddressValueError:
            raise forms.ValidationError("Invalid IPv4 address.")
        return ipv4_address


class GatewayModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.name} - {obj.serial_number} - {obj.ipv4_address}"


class PeripheralDeviceForm(forms.ModelForm):
    gateway = GatewayModelChoiceField(queryset=Gateway.objects.all())

    class Meta:
        model = PeripheralDevice
        fields = ["uid", "vendor", "status", "gateway"]
