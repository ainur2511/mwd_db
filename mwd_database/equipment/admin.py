from django.contrib import admin
from django.db.models.options import Options
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import EquipmentCategoryChangeForm, EquipmentMoveForm

from .models import *


class EquipmentAdmin(admin.ModelAdmin):
    actions = ['move_equipment', ]
    list_display = ['equipment_type',
                    'serial_number',
                    'location',
                    'vendor',
                    'inventory_number',
                    ]
    list_max_show_all = 15
    list_filter = ('equipment_type', 'location')

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


class LocationAdmin(admin.ModelAdmin):
    inlines = [EquipmentInline]


class CategoryInline(admin.StackedInline):
    model = EquipmentType
    extra = 0


class EquipmentTypeAdmin(admin.ModelAdmin):
    actions = ['change_category', ]
    list_display = ['equipment_name', 'category'
                    ]
    list_filter = [('category', admin.RelatedOnlyFieldListFilter)]
    inlines = [CategoryInline]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field == 'category':
            kwargs['queryset'] = EquipmentType.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    @admin.action(description='Изменить категорию')
    def change_category(self, request, queryset):
        form = None
        if 'apply' in request.POST:
            print(request.POST)
            form = EquipmentCategoryChangeForm(request.POST)
            if form.is_valid():
                new_category = form.cleaned_data['category']
                print(form.cleaned_data)
                for obj in queryset:
                    print(obj)
                    obj.category = new_category
                    obj.save()
                self.message_user(request, 'Категории изменены')
                return HttpResponseRedirect(request.get_full_path())
        if 'cancel' in request.POST:
            return HttpResponseRedirect(request.get_full_path())
        if not form:
            form = EquipmentCategoryChangeForm(initial={'_selected_action': queryset.values_list('id', flat=True)})

        return render(request, 'admin/change_parent_category.html', {'form': form, 'queryset': queryset, 'title': u'Изменение категории'})




    # @admin.display(description='Оборудование')
    # def get_threaded_connection(self, obj):
    #     return obj.threaded_connection.thread_type

    # @admin.display(description='Категория')
    # def get_category(self, obj):
    #     return obj.equipment_category.category

    # list_max_show_all = 15


# class OperatingTimeAdmin(admin.ModelAdmin):
#     list_display = ['get_equipment_name',
#                     'circulation',
#                     'meters',
#                     'screw_up',
#                     'operating_date'
#                     ]
#
#     @admin.display(description='')
#     def get_equipment_name(self, obj):
#         return f'{str(obj.equipment.equipment_type)} № {str(obj.equipment.serial_number)}'
#
#
#     list_max_show_all = 15


admin.site.register(EquipmentType, EquipmentTypeAdmin)
admin.site.register(Vendor)
admin.site.register(ThreadConnection)
admin.site.register(Location, LocationAdmin)
admin.site.register(Equipment, EquipmentAdmin)
