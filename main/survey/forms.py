from django import forms
from .models import Survey
from office.models import Service

class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = '__all__'
        labels = {
            'name': 'Name:',
            'office': 'Division/Office/Unit',
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

        beige_input = "px-3 py-2 rounded-full "
        widgets = {
            'office': forms.Select(attrs={
                'class': beige_input + "w-1/2",
            }),

            'email': forms.EmailInput(attrs={
                'class': beige_input + "w-1/2",
            }),

            'name': forms.TextInput(attrs={
                'class': beige_input + "w-1/4",
            }),

            'contact_number': forms.TextInput(attrs={
                'class': beige_input + "w-1/4",
            }),

            'client_type': forms.RadioSelect(attrs={
                'class': beige_input,
            }),

            'date': forms.DateInput(attrs={
                'class': beige_input + "", 'type': "date"
            }),

            'service': forms.Select(attrs={
                'class': beige_input + "w-1/2",
            }),

            'sex': forms.RadioSelect(attrs={
                'class': beige_input,
            }),

            'age': forms.NumberInput(attrs={
                'class': beige_input,
            }),

            'region': forms.TextInput(attrs={
                'class': beige_input + "w-full", 'placeholder': "Input region of residence"
            }),


            'cc1': forms.RadioSelect(attrs={
                'class': beige_input,
            }),

            'cc2': forms.RadioSelect(attrs={
                'class': beige_input,
            }),

            'cc3': forms.RadioSelect(attrs={
                'class': beige_input,
            }),

            'sqd0': forms.RadioSelect(attrs={
                'class': beige_input,
            }),
            'sqd1': forms.RadioSelect(attrs={
                'class': beige_input,
            }),
            'sqd2': forms.RadioSelect(attrs={
                'class': beige_input,
            }),
            'sqd3': forms.RadioSelect(attrs={
                'class': beige_input,
            }),
            'sqd4': forms.RadioSelect(attrs={
                'class': beige_input,
            }),
            'sqd5': forms.RadioSelect(attrs={
                'class': beige_input,
            }),
            'sqd6': forms.RadioSelect(attrs={
                'class': beige_input,
            }),
            'sqd7': forms.RadioSelect(attrs={
                'class': beige_input,
            }),
            'sqd8': forms.RadioSelect(attrs={
                'class': beige_input,
            }),

            
            'suggestions': forms.Textarea(attrs={
                'class': beige_input + "rounded-lg w-full",
            }),
        }

        help_texts = {
            'cc1': 'Which of the following best describes your awareness of a CCC?',
            'cc2': 'If aware of CC (answered 1-3 in CC1), would you say that the CC of this office was... ?',
            'cc3': 'If aware of CC (answered codes 1-3 in CC1), how much did the CC help you in your transaction?',
            'sqd0': 'I am satisfied with the service that I availed.',
            'sqd1': 'I spent a reasonable amount of time for my transaction.',
            'sqd2': 'The office followed the transaction’s requirements and steps based on the information provided.',
            'sqd3': 'The steps (including payment) I needed to do for my transaction were easy and simple.',
            'sqd4': 'I easily found information about mu transaction from the office ir its website.',
            'sqd5': 'I paid a reasonable amount of fees for my transaction.',
            'sqd6': 'I feel the office was fair to everyone, or “walang palakasan”, during my transaction.',
            'sqd7': 'I was treated courteously by the staff, and (if asked for help) the staff was helpful.',
            'sqd8': 'I got what I needed from the government office, or (if denied) denial of request was sufficiently explained to me.',
        }
    
    def __init__(self, *args, **kwargs):
        office_id = kwargs.pop('office_id', None)
        super(SurveyForm, self).__init__(*args, **kwargs)
        if office_id:
            self.fields['service'].queryset = Service.objects.filter(office_id=office_id)
