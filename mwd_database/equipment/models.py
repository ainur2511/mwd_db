from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import ForeignKey


class Equipment(models.Model):
    """ Экземпляр оборудования """
    equipment_type: ForeignKey = models.ForeignKey('EquipmentType', verbose_name='Тип оборудования',
                                                   on_delete=models.CASCADE, related_name='equipments')
    serial_number = models.CharField(max_length=25, verbose_name='Заводской номер')
    inventory_number = models.CharField(max_length=25, verbose_name='Инвентарный номер')
    vendor = models.ForeignKey('Vendor', verbose_name='Производитель', on_delete=models.CASCADE)
    location = models.ForeignKey('Location', verbose_name='Местонахождение', on_delete=models.CASCADE)

    def get_total_circulation(self):
        total_operating_time = getattr(self, 'totaloperatingtime', None)  # Используем правильное имя
        if total_operating_time:
            return total_operating_time.total_circulation
        return 'нет данных'
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


class Tag(models.Model):
    name = models.CharField(verbose_name='Тег', max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class EquipmentType(models.Model):
    """Каталог оборудования, из которых мы создаем конкретный экземпляр оборудования"""
    equipment_name = models.CharField(max_length=100, unique=True, verbose_name='Наименование оборудования')
    tags = models.ManyToManyField(Tag, verbose_name='Теги', blank=True, related_name='equipment_types')

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


class TotalOperatingTime(models.Model):
    """Суммароные наработки оборудования"""
    equipment_name = models.OneToOneField(Equipment,
                                          verbose_name='Оборудование',
                                          on_delete=models.CASCADE,
                                          related_name='totaloperatingtime')
    total_circulation = models.PositiveIntegerField(verbose_name='Часы общее', default=0)
    total_meters = models.PositiveIntegerField(verbose_name='Метры общее', default=0)
    changed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.equipment_name.equipment_type) + ' № ' + str(self.equipment_name.serial_number)

    def clean(self):
        equipment_type = self.equipment_name.equipment_type
        tags = equipment_type.tags.all()
        tag_names = [tag.name for tag in tags]
        required_tags = ('Забойное',)
        if not any(tag in tag_names for tag in required_tags):
            raise ValidationError(
                f"Оборудование '{self.equipment_name}' не имеет необходимых тегов для учета наработки.")

    class Meta:
        verbose_name = 'Общие наработки'
        verbose_name_plural = 'Общие наработки'


class AssemblyRunTime(models.Model):
    """ Рейсовая наработка """
    equipment = models.ForeignKey('TotalOperatingTime', verbose_name='Оборудование', on_delete=models.CASCADE)
    circulation = models.PositiveIntegerField(verbose_name='Часы циркуляции за рейс')
    meters = models.PositiveIntegerField(verbose_name='Пробурено метров за рейс')
    operation_date = models.DateField(verbose_name='Дата окончания рейса')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата/время добавления')
    user = models.ForeignKey(User, verbose_name='Опреатор', on_delete=models.CASCADE, related_name='user')

    def __str__(self):
        return f'{str(self.equipment)} - наработка за рейс'
    @transaction.atomic
    def save(self, *args, **kwargs):
        # Сначала вызываем метод save родительского класса
        super().save(*args, **kwargs)
        # Обновляем поля total_circulation и total_meters в связанной модели TotalOperatingTime
        total_operating_time = self.equipment  # Получаем связанную запись TotalOperatingTime
        total_operating_time.total_circulation += self.circulation  # Прибавляем часы
        total_operating_time.total_meters += self.meters  # Прибавляем метры
        total_operating_time.save()  # Сохраняем изменения

    class Meta:
        verbose_name = 'Наработка за рейс'
        verbose_name_plural = 'Наработки за рейс'
