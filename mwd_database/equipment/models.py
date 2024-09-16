from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import ForeignKey


class Equipment(models.Model):
    """ Базовый класс оборудования """
    equipment_type: ForeignKey = models.ForeignKey('EquipmentType', verbose_name='Тип оборудования',
                                                   on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=25, verbose_name='Заводской номер')
    inventory_number = models.CharField(max_length=25, verbose_name='Инвентарный номер')
    vendor = models.ForeignKey('Vendor', verbose_name='Производитель', on_delete=models.CASCADE)
    location = models.ForeignKey('Location', verbose_name='Местонахождение', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.equipment_type) + ' № ' + self.serial_number
    class Meta:
        verbose_name = 'Оборудование'
        verbose_name_plural = 'Оборудование'
        unique_together = ('equipment_type', 'serial_number',)
class Property(models.Model):
    equipment = models.ForeignKey(Equipment, verbose_name='Оборо', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Vendor(models.Model):
    """Производитель оборудования"""
    vendor_name = models.CharField(verbose_name='Производитель', max_length=150, unique=True)

    def __str__(self):
        return self.vendor_name

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'


class EquipmentType(models.Model):
    """Типы оборудования в виде иерархической структуры"""
    equipment_name = models.CharField(max_length=100, unique=True, verbose_name='Наименование оборудования')
    category = models.ForeignKey(
        'self',
        verbose_name='Родительская категория',
        related_name='children',
        on_delete=models.CASCADE,
        blank=True,
        null=True
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


class Location(models.Model):
    """Местонахождение оборудования"""
    location = models.CharField(verbose_name='Местонахождение', max_length=150, unique=True)

    def __str__(self):
        return self.location

    class Meta:
        verbose_name = 'Местонахождение'
        verbose_name_plural = 'Местонахождения'

# class OperatingTime(models.Model):
#     """ Факт внесения наработки """
#     equipment = models.ForeignKey('Equipment', verbose_name='Оборудование', on_delete=models.CASCADE)
#     circulation = models.IntegerField(verbose_name='Часы циркуляции за рейс')
#     meters = models.IntegerField(verbose_name='Пробурено метров за рейс')
#     screw_up = models.SmallIntegerField(verbose_name='Свинчиваний')
#     operating_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата/время добавления')
#
#     class Meta:
#         verbose_name = 'Наработку'
#         verbose_name_plural = 'Наработки'


# class BottomEquipment(Equipment):
#     total_circulation = models.IntegerField(verbose_name='Часы общее')
#     total_meters = models.IntegerField(verbose_name='Метры общее')
#     total_screw_up = models.SmallIntegerField(verbose_name='Свинчиваний общее')
#
#     class Meta:
#         abstract = True