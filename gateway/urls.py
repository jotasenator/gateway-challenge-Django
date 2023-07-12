from django.urls import path

from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("gateways_list", views.gateways_list, name="gateways_list"),
    path(
        "peripheral/<int:peripheral_id>/delete",
        views.peripheral_device_delete,
        name="peripheral_device_delete",
    ),
]
