from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

class CheckoutContactForm(forms.Form):
    name = forms.CharField(required=True, max_length=30, min_length=2, label='Имя', error_messages={'required': 'Укажите имя', 'max_length': 'Максимальное количество символов 30', 'min_length': 'Минимальное количество символов 2'})
    phone = forms.CharField(required=True, label='Телефон',min_length=8, max_length=15, error_messages={'required': 'Укажите ваш номер телефона','min_length': 'Минимальное количество символов 8', 'max_length': 'Максимальное количество символов 15'} )
    email = forms.EmailField(required=True, min_length=7, label='Email', error_messages={'required': 'Укажите ваш номер Email-адрес', 'min_length': 'Минимальное количество символов 7', 'invalid':'Неверно ввели Email, пример ввода: name@example.com'})
    address = forms.CharField(required=False, label='Адрес')
    comments = forms.CharField(required=False,  label='Комментарий')






