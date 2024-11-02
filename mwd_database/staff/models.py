from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    agreement_accepted = models.BooleanField(default=False)





