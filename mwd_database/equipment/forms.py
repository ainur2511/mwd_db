from django import forms
from django.contrib.auth.models import Group

from equipment.models import EquipmentType, Location


class EquipmentCategoryChangeForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    category = forms.ModelChoiceField(queryset=EquipmentType.objects.all(), label=u"Выбор категории")


class EquipmentMoveForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    location = forms.ModelChoiceField(queryset=Location.objects.all(), label=u"Куда переместить? ")

