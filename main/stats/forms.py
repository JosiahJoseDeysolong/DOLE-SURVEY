from django import forms
from survey.models import Survey
from office.models import Service

class SurveyEditForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = '__all__'
        exclude = ['office']
        labels = {
            'name': 'Name:',
            'contact_number': 'Contact Number:',
            'email': 'Email Address:',
            'client_type': 'Client Type:',
            'date': 'Date:',
            'sex': 'Sex:',
            'age': 'Age:',
            'region': 'Region of Residence',
            'service': 'Service Availed:',
            'cc1': 'CC1',
            'cc2': 'CC2',
            'cc3': 'CC3',
            'sqd0': 'SQD0',
            'sqd1': 'SQD1',
            'sqd2': 'SQD2',
            'sqd3': 'SQD3',
            'sqd4': 'SQD4',
            'sqd5': 'SQD5',
            'sqd6': 'SQD6',
            'sqd7': 'SQD7',
            'sqd8': 'SQD8',
            'suggestions': 'Suggestions on how we can further improve services',
        }

        beige_input = "px-3 py-2 rounded-full"
        widgets = {
            'email': forms.EmailInput(attrs={'class': beige_input + " w-1/2"}),
            'name': forms.TextInput(attrs={'class': beige_input + " w-full"}),
            'contact_number': forms.TextInput(attrs={'class': beige_input + " w-1/4"}),
            'client_type': forms.RadioSelect(attrs={'class': beige_input}),
            'date': forms.DateInput(attrs={'class': beige_input, 'type': "date"}),
            'service': forms.Select(attrs={'class': beige_input + " w-1/2"}),
            'sex': forms.RadioSelect(attrs={'class': beige_input}),
            'age': forms.NumberInput(attrs={'class': beige_input}),
            'region': forms.TextInput(attrs={'class': beige_input + " w-full", 'placeholder': "Input region of residence"}),
            'cc1': forms.RadioSelect(attrs={'class': beige_input}),
            'cc2': forms.RadioSelect(attrs={'class': beige_input}),
            'cc3': forms.RadioSelect(attrs={'class': beige_input}),
            'sqd0': forms.RadioSelect(attrs={'class': beige_input}),
            'sqd1': forms.RadioSelect(attrs={'class': beige_input}),
            'sqd2': forms.RadioSelect(attrs={'class': beige_input}),
            'sqd3': forms.RadioSelect(attrs={'class': beige_input}),
            'sqd4': forms.RadioSelect(attrs={'class': beige_input}),
            'sqd5': forms.RadioSelect(attrs={'class': beige_input}),
            'sqd6': forms.RadioSelect(attrs={'class': beige_input}),
            'sqd7': forms.RadioSelect(attrs={'class': beige_input}),
            'sqd8': forms.RadioSelect(attrs={'class': beige_input}),
            'suggestions': forms.Textarea(attrs={'class': beige_input + " rounded-lg w-full"}),
        }
    
    def __init__(self, *args, **kwargs):
        office_id = kwargs.pop('office_id', None)
        super(SurveyEditForm, self).__init__(*args, **kwargs)
        if office_id:
            self.fields['service'].queryset = Service.objects.filter(office_id=office_id)
