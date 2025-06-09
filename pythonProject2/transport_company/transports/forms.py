from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'items_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'departure_point': forms.TextInput(attrs={'class': 'form-control'}),
            'destination_point': forms.TextInput(attrs={'class': 'form-control'}),
            'distance': forms.NumberInput(attrs={'class': 'form-control'}),
            'trailer': forms.Select(attrs={'class': 'form-control'}),
            'driver': forms.Select(attrs={'class': 'form-control'}),
            'completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }