from django.shortcuts import render, redirect, get_object_or_404
from .models import Gateway, PeripheralDevice

from .forms import GatewayForm, PeripheralDeviceForm


# Create your views here.


def index(request):
    if request.method == "POST":
        if "gateway_submit" in request.POST:
            gateway_form = GatewayForm(request.POST, prefix="gateway")

            if gateway_form.is_valid():
                gateway_form.save()
                return redirect("gateways_list")
        else:
            gateway_form = GatewayForm(prefix="gateway")

        if "peripheral_device_submit" in request.POST:
            peripheral_device_form = PeripheralDeviceForm(
                request.POST, prefix="peripheral_device"
            )

            if peripheral_device_form.is_valid():
                peripheral_device_form.save()
                return redirect("gateways_list")
        else:
            peripheral_device_form = PeripheralDeviceForm(prefix="peripheral_device")

    else:
        gateway_form = GatewayForm(prefix="gateway")
        peripheral_device_form = PeripheralDeviceForm(prefix="peripheral_device")

    return render(
        request,
        "gateway/index.html",
        {
            "gateway_form": gateway_form,
            "peripheral_device_form": peripheral_device_form,
        },
    )


def gateways_list(request):
    all_gateways = Gateway.objects.all()
    gateway_data = []
    for gateway in all_gateways:
        peripherals = gateway.peripheral_devices.all()
        peripheral_data = []
        for peripheral in peripherals:
            peripheral_data.append(
                {
                    "id": peripheral.id,
                    "uid": peripheral.uid,
                    "vendor": peripheral.vendor,
                    "status": peripheral.status,
                    "date_created": peripheral.date_created,
                }
            )
        gateway_data.append(
            {
                "id": gateway.id,
                "serial_number": gateway.serial_number,
                "name": gateway.name,
                "ipv4_address": gateway.ipv4_address,
                "peripherals": peripheral_data,
            }
        )
    return render(request, "gateway/gateways_list.html", {"gateway_data": gateway_data})


def peripheral_device_delete(request, peripheral_id):
    if request.method == "POST":
        peripheral = get_object_or_404(PeripheralDevice, pk=peripheral_id)
        peripheral.delete()
    return redirect("gateways_list")
