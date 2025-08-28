from django import forms
from .models import Feeder

class FeederForm(forms.ModelForm):
    class Meta:
        model = Feeder
        fields = ['name']
