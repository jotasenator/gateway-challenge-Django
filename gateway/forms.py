from django import forms
from .models import Gateway, PeripheralDevice

from django.forms import ModelChoiceField

import ipaddress

from django.forms.utils import ErrorList

from django.core.exceptions import ValidationError


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

    def clean(self):
        cleaned_data = super().clean()
        gateway = cleaned_data.get("gateway")
        if gateway and gateway.peripheral_devices.count() == 10:
            raise ValidationError(
                "A gateway can have a maximum of 10 peripheral devices."
            )
        return cleaned_data

    # minimum value of the input type number for uid is 0
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["uid"].widget.attrs.update({"min": "0"})


# overwriting errorList style
class AlertErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return ""
        return f'<div class="text-danger" role="alert">{super().as_ul()}</div>'
