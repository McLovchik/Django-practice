from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PersonalCabinet


class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')


class ExtendedRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Имя')
    last_name = forms.CharField(max_length=30, required=False, help_text='Фамилия')
    city = forms.CharField(max_length=36, required=False, help_text='Город')
    phone = forms.CharField(max_length=11, required=False, help_text='Телефон')
    # verification_flag = forms.BooleanField()
    # count_news = forms.IntegerField()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'city', 'phone', 'password1', 'password2',)


class ReplenishTheBalanceForm(forms.ModelForm):
    class Meta:
        model = PersonalCabinet
        fields = ('balance',)
        labels = {
            'balance': 'Сумма пополнения'
        }
