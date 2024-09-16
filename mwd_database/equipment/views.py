from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import UpdateView

from equipment.forms import EquipmentCategoryChangeForm
from equipment.models import Equipment, EquipmentType



