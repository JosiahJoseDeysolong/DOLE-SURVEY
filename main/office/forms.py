from django import forms
from .models import Office, Service

class OfficeForm(forms.ModelForm):
    class Meta:
        model = Office
        fields = '__all__'
        labels = {
            'office_name': 'Office Name:',
            'office_description': 'Office Description:',
        }

        beige_input = "px-3 py-2 rounded-full "
        widgets = {
            'office_name': forms.TextInput(attrs={
                'class': beige_input + "w-full",
            }),
            'office_description': forms.Textarea(attrs={
                'class': beige_input + "w-full rounded-lg",
            }),
        }


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ('service_name', 'service_description') 
        labels = {
            'service_name': 'Service Name:',
            'service_description': 'Service Description:',
        }

        beige_input = "px-3 py-2 rounded-full "

        widgets = {
            'service_name': forms.TextInput(attrs={
                'class': beige_input + "w-full",
            }),
            'service_description': forms.Textarea(attrs={
                'class': beige_input + "w-full rounded-lg",
            }),
        }