from django.urls import path
from helusers.admin_site import admin

urlpatterns = [path("admin/", admin.site.urls)]
