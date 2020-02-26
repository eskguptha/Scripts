from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.conf import settings
from accounts.models import Devices, MarketPlace

admin.site.unregister(Group)
admin.site.unregister(User)

class DevicesAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'connection_type','port' ,'updated_at')
    def has_add_permission(self, request, obj=None):
        if Devices.objects.all().count() > 1:
            return False
        else:
            return True
    pass

class MarketPlaceAdmin(admin.ModelAdmin):
    actions = None
    list_display = ('name', 'created_at', 'ipaddress','port' ,'updated_at')
    def has_add_permission(self, request, obj=None):
        if MarketPlace.objects.all().count() > 0:
            return False
        else:
            return True
    def has_delete_permission(self, request, obj=None):
        return False
    pass

class UserAdmin(admin.ModelAdmin):
    actions = None
    def has_add_permission(self, request, obj=None):
        if User.objects.all().count() > 0:
            return False
        else:
            return False

    def has_delete_permission(self, request, obj=None):
        return False

    pass


admin.site.register(User, UserAdmin)
admin.site.register(Devices, DevicesAdmin)
admin.site.register(MarketPlace, MarketPlaceAdmin)
