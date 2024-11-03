from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.safestring import mark_safe

from equipment.models import Equipment, EquipmentType, Tag


class ThreadInspection(models.Model):
    equipment_name = models.OneToOneField(Equipment, on_delete=models.CASCADE)
    inspection_date = models.DateField()

    def clean(self):
        equipment_type = self.equipment_name.equipment_type
        tags = equipment_type.tags.all()
        tag_names = [tag.name for tag in tags]
        required_tags = ('Корпусное',)
        if not any(tag in tag_names for tag in required_tags):
            raise ValidationError(
                f"Оборудование '{self.equipment_name}' не имеет необходимых тегов для учета наработки.")

    def days_until_next_inspection(self):
        next_inspection_date = self.inspection_date + timezone.timedelta(days=180)
        days_remaining = (next_inspection_date - timezone.now().date()).days
        return days_remaining

    def inspection_status(self):
        days_remaining = self.days_until_next_inspection()

        if days_remaining > 180:
            return mark_safe('<span style="color: green;">В Норме</span>')
        elif 30 < days_remaining <= 180:
            return mark_safe('<span style="color: green;">В Норме</span>')
        elif 0 <= days_remaining <= 30:
            return mark_safe('<span style="color: orange;">ОБРАТИТЬ ВНИМАНИЕ!</span>')
        else:
            return mark_safe('<span style="color: red;">ПРОСРОЧЕНО!</span>')

    days_until_next_inspection.short_description = 'Осталось дней до следующей инспекции'
    inspection_status.short_description = 'Статус инспекции'


class Maintenance(models.Model):
    STATUS_CHOICES = (('IN_PROGRESS', 'В работе'),
                      ('COMPLETED', 'Завершен'))
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='maintenance')
    start_date = models.DateField(verbose_name='Дата начала TO/ремонта')
    end_date = models.DateField(verbose_name='Дата окончания TO/ремонта', null=True, blank=True)
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    status = models.CharField(verbose_name='Статус ремонта', choices=STATUS_CHOICES, default='IN_PROGRESS')

    def save(self, *args, **kwargs):
        # Сначала вызываем метод save родительского класса
        super().save(*args, **kwargs)
        # Обновляем статус оборудования в зависимости от статуса ремонта
        if self.status == 'IN_PROGRESS':
            self.equipment.stop_status = 'REPAIR'
        elif self.status == 'COMPLETED':
            self.equipment.stop_status = 'NORMAL'
        # Сохраняем обновленный статус оборудования
        self.equipment.save(update_fields=['stop_status'])  # Сохраняем только измененное поле

