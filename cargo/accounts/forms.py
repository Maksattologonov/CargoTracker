from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('gmail', 'phone_number', 'first_name', 'last_name')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('gmail', 'phone_number', 'first_name', 'last_name')


class CustomAuthenticationForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ('email', 'password')


class UserRegisterForm(forms.ModelForm):
    phone_number = forms.CharField(label='Phone Number', min_length=9, max_length=14)

    class Meta:
        model = CustomUser
        exclude = ('password', 'password2')
        fields = ('gmail', 'phone_number', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['gmail'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['gmail'].widget.attrs['style'] = 'font-family:Arial, FontAwesome'
        self.fields['phone_number'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['first_name'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['last_name'].widget.attrs['class'] = 'form-control form-control-lg'

    labels = {
        'name': _('form-control form-control-lg'),
    }
    help_texts = {
        'name': _('Some useful help text.'),
    }
    error_messages = {
        'name': {
            'max_length': _("This writer's name is too long."),
        },
    }