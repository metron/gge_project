from django import forms
from .models import Estimate

class EstimateUploadForm(forms.ModelForm):
    class Meta:
        model = Estimate
        fields = ['title', 'file']  # Пользователь заполняет только эти два поля

