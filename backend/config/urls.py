from django.contrib import admin
from django.urls import path
from vpn.views import DevicesView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/devices/', DevicesView.as_view()),
]
