from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

from .models import CalorieEntry, Profile

User = get_user_model()


class RegistrationForm(forms.ModelForm):
 
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'email': forms.EmailInput(),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class EmailOrUsernameAuthenticationForm(AuthenticationForm):
   
    username = forms.CharField(label='Username or Email')


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['name', 'age', 'gender', 'height_cm', 'weight_kg', 'activity_level', 'goal']
        widgets = {
            'gender': forms.Select(),
            'activity_level': forms.Select(),
            'goal': forms.Select(),
        }
        labels = {
            'height_cm': 'Height (cm)',
            'weight_kg': 'Weight (kg)',
        }


class CalorieEntryForm(forms.ModelForm):

    class Meta:
        model = CalorieEntry
        fields = ['item_name', 'calories', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
