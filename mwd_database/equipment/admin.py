from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from simple_history.admin import SimpleHistoryAdmin

from .forms import EquipmentMoveForm
from django_admin_multi_select_filter.filters import MultiSelectFieldListFilter

from .models import *


class TagFilter(admin.SimpleListFilter):
    title = 'Теги'
    parameter_name = 'tags'

    def lookups(self, request, model_admin):
        tags = Tag.objects.all()
        return [(tag.id, tag.name) for tag in tags]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(equipment_type__tags__id=self.value())
        return queryset


@admin.register(Equipment)
class EquipmentAdmin(SimpleHistoryAdmin):
    actions = ['move_equipment', ]
    list_display = ['equipment_type',
                    'serial_number',
                    'location',
                    'vendor',
                    'inventory_number',
                    'get_total_circulation',
                    'stop_status',
                    ]
    list_max_show_all = 15
    list_filter = ('equipment_type', 'location', TagFilter)


    @admin.action(description='Переместить оборудование')
    def move_equipment(self, request, queryset):
        form = None
        if 'apply' in request.POST:
            form = EquipmentMoveForm(request.POST)
            if form.is_valid():
                new_location = form.cleaned_data['location']
                print(form.cleaned_data)
                for obj in queryset:
                    print(obj)
                    obj.location = new_location
                    obj.save()
                self.message_user(request, 'Оборудование перемещено')
                return HttpResponseRedirect(request.get_full_path())
        if 'cancel' in request.POST:
            return HttpResponseRedirect(request.get_full_path())
        if not form:
            form = EquipmentMoveForm(initial={'_selected_action': queryset.values_list('id', flat=True)})

        return render(request, 'admin/equipmet_move_form.html',
                      {'form': form, 'queryset': queryset, 'title': u'Перемещение оборудования'})


class EquipmentInline(admin.TabularInline):
    model = Equipment
    extra = 0
    max_num = 0
    fields = ('equipment_type', 'serial_number',)
    readonly_fields = ['equipment_type', 'serial_number', ]

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Location)
class LocationAdmin(SimpleHistoryAdmin):
    inlines = [EquipmentInline]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'well_number':
            kwargs['queryset'] = Well.objects.filter(is_active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Well)
class WellAdmin(SimpleHistoryAdmin):
    list_display = ('well_number', 'created_at', 'updated_at', 'is_active')


@admin.register(EquipmentType)
class EquipmentTypeAdmin(SimpleHistoryAdmin):
    actions = []
    list_display = ['equipment_name', 'get_tags'
                    ]
    filter_horizontal = ('tags',)

    def get_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])  # Получаем имена тегов

    get_tags.short_description = 'Теги'  # Заголовок колонки в админке
    list_filter = [('tags__name', MultiSelectFieldListFilter)]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field == 'category':
            kwargs['queryset'] = EquipmentType.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class AssemblyRunTimeInline(admin.TabularInline):
    model = AssemblyRunTime
    extra = 0
    fields = ('equipment', 'circulation', 'meters', 'operation_date', 'user',)
    readonly_fields = ['equipment',]

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(TotalOperatingTime)
class TotalOperatingTimeAdmin(SimpleHistoryAdmin):
    list_display = ['equipment_name', 'total_circulation', 'total_meters', 'changed_at']
    readonly_fields = ['equipment_name', 'total_circulation', 'total_meters']
    ordering = ['-changed_at']
    inlines = [AssemblyRunTimeInline]


@admin.register(AssemblyRunTime)
class AssemblyRunTimeAdmin(SimpleHistoryAdmin):
    list_display = ('equipment', 'circulation', 'meters', 'operation_date', 'user', )


admin.site.site_header = 'ALGIS MWD Database'
admin.site.site_title = 'ALGIS MWD'
admin.site.index_title = 'Управление сайтом'
