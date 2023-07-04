from django.contrib import admin
from .models import *
# Register your models here.


class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['equipment_type', 'serial_number', 'get_vendor']

    @admin.display(description='Производитель')
    def get_vendor(self, obj):
        return obj.equipment_type.vendor
    list_max_show_all = 15
    list_filter = ('equipment_type',)


admin.site.register(EquipmentType)
admin.site.register(Vendor)
admin.site.register(ThreadConnection)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(EquipmentCategory)