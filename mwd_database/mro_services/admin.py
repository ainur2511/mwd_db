from django.contrib import admin

from mro_services.models import ThreadInspection, Maintenance


@admin.register(ThreadInspection)
class ThreadInspectionAdmin(admin.ModelAdmin):
    list_display = ('equipment_name',
                    'inspection_date',
                    'days_until_next_inspection',
                    'inspection_status',
                    )

@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ('equipment',
                    'start_date',
                    'end_date',
                    'status',
                    'description')