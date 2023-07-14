from django.shortcuts import render, redirect, get_object_or_404
from .models import Gateway, PeripheralDevice

from .forms import GatewayForm, PeripheralDeviceForm, AlertErrorList

from django.contrib import messages

from natsort import natsorted

import json
from django.http import JsonResponse

# Create your views here.


def index(request):
    if request.method == "POST":
        if "gateway_submit" in request.POST:
            gateway_form = GatewayForm(
                request.POST, error_class=AlertErrorList, prefix="gateway"
            )

            if gateway_form.is_valid():
                gateway = gateway_form.save()
                messages.success(request, f"New gateway added! {gateway.name}")
                return redirect("gateways_list")
        else:
            gateway_form = GatewayForm(prefix="gateway")

        if "peripheral_device_submit" in request.POST:
            peripheral_device_form = PeripheralDeviceForm(
                request.POST, prefix="peripheral_device"
            )

            if peripheral_device_form.is_valid():
                peripheral = peripheral_device_form.save()
                messages.success(
                    request,
                    f"New peripheral device added! <b>{peripheral.vendor}</b> to gateway <b>{peripheral.gateway.name}</b>",
                )
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
    sorted_gateways = natsorted(all_gateways, key=lambda x: x.name)
    gateway_data = []
    for gateway in sorted_gateways:
        peripherals = gateway.peripheral_devices.all().order_by("uid")
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


# if i send data from javascript as json-->

# def update_device_status(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         print(data)
#         id = data.get('id')
#         print(id)
#         new_status = data.get('peripheral_status')
#         try:
#             device = PeripheralDevice.objects.get(id=id)
#             device.status = new_status
#             device.save()
#             return JsonResponse({'status': 'success'})
#         except PeripheralDevice.DoesNotExist:
#             return JsonResponse({'status': 'error', 'message': 'Device not found'})
#     else:
#         return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def update_device_status(request):
    if request.method == "POST":
        peripheral_id = request.POST.get("id")
        print(f"peripheral_id {peripheral_id}")
        peripheral_status = request.POST.get("peripheral_status")
        print(f"peripheral_status {peripheral_status}")
        peripheral = get_object_or_404(PeripheralDevice, pk=peripheral_id)
        peripheral.status = peripheral_status
        peripheral.save()
    return redirect("gateways_list")


def check_uid_exists(request, uid):
    exists = PeripheralDevice.objects.filter(uid=uid).exists()
    next_uid = uid
    while PeripheralDevice.objects.filter(uid=next_uid).exists():
        next_uid += 1
    return JsonResponse({"exists": exists, "next_uid": next_uid})
