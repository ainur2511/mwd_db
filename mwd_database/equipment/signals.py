from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import AssemblyRunTime, TotalOperatingTime


@receiver(post_save, sender=AssemblyRunTime)
def update_total_operating_time(sender, instance, created, **kwargs):
    if created:
        with transaction.atomic():
            total_operating_time = instance.equipment  # Получаем связанную запись TotalOperatingTime
            total_operating_time.total_circulation += instance.circulation  # Прибавляем часы
            total_operating_time.total_meters += instance.meters  # Прибавляем метры
            total_operating_time.save()  # Сохраняем изменения