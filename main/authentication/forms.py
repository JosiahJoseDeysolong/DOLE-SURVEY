from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from survey.models import Office

class UserCreateForm(UserCreationForm):
    office = forms.ModelChoiceField(queryset=Office.objects.all(), required=True, 
        widget=forms.Select(attrs={
            'class': 'text-navyBlue px-3 py-2 rounded-full border border-gray-300 focus:outline-none focus:ring focus:border-blue-300 w-full'
        }))

    # Explicitly declare password1 and password2 with custom widgets
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'text-navyBlue px-3 py-2 rounded-full border border-gray-300 focus:outline-none focus:ring focus:border-blue-300 w-full',
            'placeholder': 'Password',
        }),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'text-navyBlue px-3 py-2 rounded-full border border-gray-300 focus:outline-none focus:ring focus:border-blue-300 w-full',
            'placeholder': 'Confirm Password',
        }),
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        beige_input = "text-navyBlue px-3 py-2 rounded-full border border-navyBlue focus:outline-none focus:ring focus:border-navyBlue w-full"

        widgets = {
            'username': forms.TextInput(attrs={
                'class': beige_input,
                'placeholder': 'Username',
            }),
            'first_name': forms.TextInput(attrs={
                'class': beige_input,
                'placeholder': 'First Name',
            }),
            'last_name': forms.TextInput(attrs={
                'class': beige_input,
                'placeholder': 'Last Name',
            }),
            'email': forms.EmailInput(attrs={
                'class': beige_input,
                'placeholder': 'Email Address',
            }),
        }

        help_texts = {
            'username': '',  # Remove help text for the username field
        }
