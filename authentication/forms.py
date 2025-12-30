from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(forms.ModelForm):
    """
    Admin panelda yangi foydalanuvchi yaratishda
    password1/password2 talab qilinmaydi.
    """
    class Meta:
        model = CustomUser
        fields = ('phone_number', 'role', 'is_staff', 'is_active')

class CustomUserChangeForm(forms.ModelForm):
    """
    Foydalanuvchi ma'lumotlarini o'zgartirish uchun form
    """
    class Meta:
        model = CustomUser
        fields = ('phone_number', 'first_name', 'last_name', 'role', 'is_staff', 'is_active', 'is_superuser')

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from .models import CustomUser

class PhoneAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Phone Number', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '+998901234567'
    }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your password'
    }))

    def clean_username(self):
        phone_number = self.cleaned_data.get('username')
        if not phone_number.startswith('+'):
            phone_number = '+998' + phone_number.lstrip('998')
        return phone_number

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('phone_number', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control', 'placeholder': '+998901234567'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})