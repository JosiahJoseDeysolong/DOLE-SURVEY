from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from survey.models import Office
from .models import Profile

beige_input = "text-navyBlue px-3 py-2 rounded-full border border-navyBlue focus:outline-none focus:ring focus:border-navyBlue w-full"

class UserCreateForm(UserCreationForm):
    office = forms.ModelChoiceField(
        queryset=Office.objects.all(), 
        required=True, 
        widget=forms.Select(attrs={'class': beige_input})
    )
    
    role = forms.ChoiceField(
        choices=Profile.role_choices, 
        required=True,
        widget=forms.Select(attrs={'class': beige_input})
    )

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': beige_input,
            'placeholder': 'Password',
        }),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': beige_input,
            'placeholder': 'Confirm Password',
        }),
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'office', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'class': beige_input, 'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'class': beige_input, 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': beige_input, 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': beige_input, 'placeholder': 'Email Address'}),
        }
        help_texts = {'username': ''}

class CustomUserChangeForm(UserChangeForm):
    office = forms.ModelChoiceField(
        queryset=Office.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': beige_input})
    )

    role = forms.ChoiceField(
        choices=Profile.role_choices,
        required=True,
        widget=forms.Select(attrs={'class': beige_input})
    )

    password1 = forms.CharField(
        label="New Password",
        required=False,
        widget=forms.PasswordInput(attrs={'class': beige_input, 'placeholder': 'New Password (leave blank if unchanged)'})
    )
    
    password2 = forms.CharField(
        label="Confirm New Password",
        required=False,
        widget=forms.PasswordInput(attrs={'class': beige_input, 'placeholder': 'Confirm New Password (leave blank if unchanged)'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'office', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'class': beige_input, 'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'class': beige_input, 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': beige_input, 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': beige_input, 'placeholder': 'Email Address'}),
        }
        help_texts = {'username': ''}

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                self.add_error('password2', "Passwords don't match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password1 = self.cleaned_data.get('password1')
        
        if password1:
            user.set_password(password1)
        
        if commit:
            user.save()
        
        return user
