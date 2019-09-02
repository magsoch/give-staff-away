from django import forms
from django.contrib.auth.models import User, Group
from django.forms import ModelForm

from .models import Charity, LOCATION, Help


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(
            attrs={'placeholder': 'Email'}))
    password = forms.CharField(
        label="Hasło",
        widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}),
    )


class SignUpForm(forms.Form):
    username = forms.CharField(
        label='Nazwa użytkownika',
        widget=forms.TextInput(
            attrs={'placeholder': 'Nazwa użytkownika'}
        )
    )
    first_name = forms.CharField(
        label='Imię',
        widget=forms.TextInput(
            attrs={'placeholder': 'Imię'}
        )
    )
    last_name = forms.CharField(
        label='Nazwisko',
        widget=forms.TextInput(
            attrs={'placeholder': 'Nazwisko'}
        )
    )
    email = forms.CharField(
        label='Email',
        widget=forms.EmailInput(
            attrs={'placeholder': 'Email'}
        )
    )
    password1 = forms.CharField(
        label='Hasło',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Hasło'}
        )
    )
    password2 = forms.CharField(
        label='Powtórz hasło',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Powtórz hasło'}
        )
    )


class SetAdminPermissionForm(forms.Form):
    user = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(groups__name='Użytkownik'),
        label='Użytkownik',
    )


class AddAdminForm(ModelForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']


class AddCharityForm(ModelForm):

    class Meta:
        model = Charity
        fields = '__all__'

    charity_name = forms.CharField(
        label='Nazwa organizacji',
        widget=forms.TextInput(
            attrs={'placeholder': 'Nazwa organizacji'}
        )
    )
    location = forms.Select(
        choices=LOCATION,
    )
    help = forms.ModelMultipleChoiceField(
        queryset=Help.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )


class ModifyProfileForm(ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    first_name = forms.CharField(
        label='Imię',
        widget=forms.TextInput(
            attrs={'placeholder': 'Imię'}
        )
    )
    last_name = forms.CharField(
        label='Nazwisko',
        widget=forms.TextInput(
            attrs={'placeholder': 'Nazwisko'}
        )
    )
    email = forms.CharField(
        label='Email',
        widget=forms.EmailInput(
            attrs={'placeholder': 'Email'}
        )
    )


class ChangePasswordForm(forms.Form):

    password = forms.CharField(
        label='Stare hasło',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Stare hasło'})
        )
    new_password = forms.CharField(
        label='Nowe hasło',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Nowe hasło'})
    )
    check_password = forms.CharField(
        label='Powtórz hasło',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Powtórz hasło'})
    )
