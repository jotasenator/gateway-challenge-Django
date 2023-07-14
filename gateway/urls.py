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
    path(
        "update_device_status/", views.update_device_status, name="update_device_status"
    ),
    path(
        "check_uid_exists/<int:uid>",
        views.check_uid_exists,
        name="check_uid_exists",
    ),
]
