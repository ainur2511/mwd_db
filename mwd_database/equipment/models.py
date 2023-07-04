from django.db import models
from django.db.models import ForeignKey


class Equipment(models.Model):
    """"Экземпляр конкретного типа оборудования """
    equipment_type: ForeignKey = models.ForeignKey('EquipmentType', verbose_name='Тип оборудования',
                                                   on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=25, verbose_name='Заводской номер')

    def __str__(self):
        return f'{str(self.equipment_type)} № {str(self.serial_number)}'

    class Meta:
        verbose_name = 'Оборудование'
        verbose_name_plural = 'Оборудование'


class EquipmentType(models.Model):
    """Тип оборудования"""
    equipment_name = models.CharField(max_length=100, unique=True, verbose_name='Наименование оборудования')
    vendor = models.ForeignKey('Vendor', verbose_name='Производитель', on_delete=models.CASCADE, null=True)
    is_hull = models.BooleanField(verbose_name='Корпусное', null=True)
    TYPES = [('SURF', 'Наземное'), ('BOTTOM', 'Забойное')]
    type = models.CharField(max_length=6, choices=TYPES, null=True)
    threaded_connection = models.ForeignKey(
        'ThreadConnection',
        verbose_name='Замковая резьба',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    equipment_category = models.ForeignKey(
        'EquipmentCategory',
        verbose_name='Категория',
        on_delete=models.CASCADE,
        null=True, blank=True
    )

    def __str__(self):
        return self.equipment_name

    class Meta:
        verbose_name = 'Тип оборудования'
        verbose_name_plural = 'Типы оборудования'


class ThreadConnection(models.Model):
    """Замковая резьба"""
    thread_type = models.CharField(
        verbose_name='Замковая резьба',
        max_length=10,
        unique=True,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.thread_type

    class Meta:
        verbose_name = 'Замковая резьба'
        verbose_name_plural = 'Замковые резьбы'


class EquipmentCategory(models.Model):
    """ Категория оборудования """
    category = models.CharField(
        verbose_name='Категория',
        max_length=30,
        unique=True,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Vendor(models.Model):
    """Производитель оборудования"""
    vendor_name = models.CharField(verbose_name='Производитель', max_length=150, unique=True)

    def __str__(self):
        return self.vendor_name

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'
