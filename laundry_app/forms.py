from django import forms
from .models import LaundryOrder

class LaundryOrderForm(forms.ModelForm):
    class Meta:
        model = LaundryOrder
        fields = ['name', 'address', 'whatsapp', 'laundry_type', 'pickup_date', 'pickup_time']
        widgets = {
            'pickup_date': forms.DateInput(attrs={'type': 'date'}),
            'pickup_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class TrackOrderForm(forms.Form):
    e_invoice_number = forms.CharField(max_length=20, label='E-Faktur Number')
