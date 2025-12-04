from django.contrib import admin
from .models import User, Plan, Subscription, Device, Server, ActiveSession

admin.site.register(User)
admin.site.register(Plan)
admin.site.register(Subscription)
admin.site.register(Device)
admin.site.register(Server)
admin.site.register(ActiveSession)
