import hashlib
import datetime
from django.template import Context
from django import forms
from django.conf.global_settings import MEDIA_ROOT
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm,PasswordResetForm, SetPasswordForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.forms.utils import ErrorList
from django.template import Template
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext as _
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.edit import FormView
from django.contrib.auth.forms import PasswordChangeForm
# from .models import Profile

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email',help_text="Это поле обязательно! Шаблон ввода: name@example.com")
    username = forms.CharField(required=True, max_length=15, label='Логин', help_text="Это поле обязательно! Максимальное количество символов 15.", min_length=2, error_messages={'required': 'Укажите имя', 'max_length': 'Максимальное количество символов 30', 'min_length': 'Минимальное количество символов 2'})
    password1 = forms.CharField(required=True, max_length=30, label='Пароль', help_text="Это поле обязательно!"
                                                                                        " Минимальное количество символов 8. "
                                                                                        "Пароль должен состоять из цифр и букв латинского алфавита."
                                                                                        " Максимальное количество символов 30.", min_length=8, error_messages={'required': 'Введите пароль', 'max_length': 'Максимальное количество символов 30', 'min_length': 'Минимальное количество символов 8'})
    password2 = forms.CharField(required=True, max_length=30, label='Повторите пароль', help_text="Подтвердите пароль", min_length=8, error_messages={'required': 'Подтвердите пароль!','max_length': 'Максимальное количество символов 30', 'min_length': 'Минимальное количество символов 8'})
    firstname = forms.CharField(required=True, max_length=25, help_text="Это поле обязательно.",label='Номер телефона',
                                min_length=10, error_messages={'required': 'Введите номер телефона!',
                                                              'max_length': 'Максимальное количество символов 15',
                                                              'min_length': 'Минимальное количество символов 10'})
#############################
    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password1 != password2:
            self._errors['password2'] = ErrorList([u"Пароли не совпадают."])

        return self.cleaned_data
##################################

    error_messages = {
        'password_mismatch': ("Пароли не совпадают."),
        'error': ("Форма не валидна."),
        'username_exists': _("Пользователь с таким именем уже существует."),
    }

    class Meta:
        model = User
        fields = (
            'username',
            'firstname',
            'email',
            'password1',
            'password2'
       )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        try:
            User._default_manager.get(username=username)
            # if the user exists, then let's raise an error message
            raise forms.ValidationError(
                self.error_messages['username_exists'],  # my error message
                code='username_exists',  # set the error message key
            )
        except User.DoesNotExist:
            return username  # if user does not exist so we can continue the registration process

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'mask-email form-control','placeholder': 'name@example.com'})
        self.fields['firstname'].widget.attrs.update({'class': 'mask-phone form-control', 'placeholder': '+7 (___) ___-__-__'})
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['firstname']
        user.password1 = self.cleaned_data['password1']
        user.password2 = self.cleaned_data['password2']
        user.is_active = False

        if commit:
            user.save()
        return user
    # def save(self, datas):
    #     # user = super(RegistrationForm, self).save(commit=False)
    #     #     user.email = self.cleaned_data['email']
    #     #     user.first_name = self.cleaned_data['firstname']
    #     #     user.password1 = self.cleaned_data['password1']
    #     #     user.password2 = self.cleaned_data['password2']
    #     u = User.objects.create_user(self.cleaned_data['username'],
    #                                      self.cleaned_data['email'],
    #                                      # self.cleaned_data['firstname'],
    #                                      self.cleaned_data['password1'])
    #                                      # self.cleaned_data['password2'])
    #     u.is_active = False
    #     u.save()
    #     profile = Profile()
    #     profile.user = u
    #     profile.activation_key = datas['activation_key']
    #     profile.key_expires = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=2),
    #                                                          "%Y-%m-%d %H:%M:%S")
    #     profile.save()
    #     return u
    #
    # def sendEmail(self, datas):
    #     link = "http://localhost:8000/activate/" + datas['activation_key']
    #     c = Context({'activation_link': link, 'username': datas['username']})
    #     # f = open(MEDIA_ROOT + datas['email_path'], 'r')
    #     f = open('accounts/email_msg.txt', "r", encoding="utf-8")
    #     t = Template(f.read())
    #     f.close()
    #     message = t.render(c)
    #     # print unicode(message).encode('utf8')
    #     send_mail(datas['email_subject'], message, 'scherbakov@atc-basis.ru', [datas['email']],
    #                   fail_silently=False)


class MyActivationCodeForm(forms.Form):
    error_css_class = 'has-error'
    error_messages = {'password_incorrect':
                          ("Старый пароль не верный. Попробуйте еще раз."),
                      'password_mismatch':
                          ("Пароли не совпадают."),
                      'cod-no':
                          ("Код не совпадает."),}


    def __init__(self, *args, **kwargs):
        super(MyActivationCodeForm, self).__init__(*args, **kwargs)

    code = forms.CharField(required=True, max_length=50, label='Код подтвержения', widget=forms.PasswordInput(attrs={'class': 'form-control'}),  error_messages={'required': 'Введите код!','max_length': 'Максимальное количество символов 50'})



    def save(self, commit=True):
        profile = super(MyActivationCodeForm, self).save(commit=False)
        profile.code = self.cleaned_data['code']

        if commit:
            profile.save()
        return profile


# class SignupForm(UserCreationForm):
#     email = forms.EmailField(max_length=200, help_text='Required')
#
#     class Meta:
#         model = User
#         fields = ('email', 'first_name', 'last_name')


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control login-username-input', 'placeholder': 'Введите логин'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control login-password-input',
            'placeholder': 'Введите пароль',
        }

))

class MyChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(MyChangePasswordForm, self).__init__(*args, **kwargs)

    error_css_class = 'has-error'
    error_messages = {'password_incorrect':
                          ("Старый пароль не верный. Попробуйте еще раз."),
                      'password_mismatch':
                          ("Пароли не совпадают."),}
    old_password = forms.CharField(required=True, max_length=30, label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}), help_text="Введите текущий пароль", min_length=8, error_messages={'required': 'Введите пароль!','max_length': 'Максимальное количество символов 30', 'min_length': 'Минимальное количество символов 8'})

    new_password1 = forms.CharField(required=True, max_length=30, label='Новый пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}), help_text="Пароль должен содержать не менее 8 символов.", min_length=8, error_messages={'required': 'Введите новый пароль!','max_length': 'Максимальное количество символов 30', 'min_length': 'Минимальное количество символов 8'})

    new_password2 = forms.CharField(required=True, max_length=30, label='Подтвердите новый пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}), min_length=8, error_messages={'required': 'Подтвердите пароль!','max_length': 'Максимальное количество символов 30', 'min_length': 'Минимальное количество символов 8'})


class MyPasswordResetForm(PasswordResetForm):

    def __init__(self, *args, **kwargs):
        super(MyPasswordResetForm, self).__init__(*args, **kwargs)
    email = forms.EmailField(required=True, label='Email', help_text="Для сброса пароля введите ваш Email", widget=forms.EmailInput(attrs={'class': 'form-control'}), error_messages={'required': 'Введие email!'})

class MyPasswordResetConfirmForm(SetPasswordForm):
    error_messages = {'password_incorrect':
                          ("Старый пароль не верный. Попробуйте еще раз."),
                      'password_mismatch':
                          ("Пароли не совпадают."),}

    new_password1 = forms.CharField(required=True, max_length=30, label='Новый пароль',
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                    help_text="Пароль должен содержать не менее 8 символов.", min_length=8,
                                    error_messages={'required': 'Введите новый пароль!',
                                                    'max_length': 'Максимальное количество символов 30',
                                                    'min_length': 'Минимальное количество символов 8'})

    new_password2 = forms.CharField(required=True, max_length=30, label='Подтвердите новый пароль',
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'}), min_length=8,
                                    error_messages={'required': 'Подтвердите пароль!',
                                                    'max_length': 'Максимальное количество символов 30',
                                                    'min_length': 'Минимальное количество символов 8'})

