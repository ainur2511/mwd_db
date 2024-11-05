from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords


class Profile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    agreement_accepted = models.BooleanField(default=False)
    history = HistoricalRecords()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Персонал'






