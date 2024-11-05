from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from equipment.models import Equipment
from mro_services.models import ThreadInspection, Maintenance


@admin.register(ThreadInspection)
class ThreadInspectionAdmin(SimpleHistoryAdmin):
    list_display = ('equipment_name',
                    'inspection_date',
                    'days_until_next_inspection',
                    'inspection_status',
                    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "equipment_name":
            # Фильтруем Equipment по тегу
            kwargs["queryset"] = Equipment.objects.filter(equipment_type__tags__name='Корпусное')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Maintenance)
class MaintenanceAdmin(SimpleHistoryAdmin):
    list_display = ('equipment',
                    'start_date',
                    'end_date',
                    'status',
                    'description')