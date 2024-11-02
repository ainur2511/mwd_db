from django import forms

from equipment.models import Location


class EquipmentMoveForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    location = forms.ModelChoiceField(queryset=Location.objects.all(), label=u"Куда переместить? ")

