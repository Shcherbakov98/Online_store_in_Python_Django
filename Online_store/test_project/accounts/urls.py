"""test_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import  settings
from . import views
from .forms import UserLoginForm, MyChangePasswordForm, MyPasswordResetForm, MyPasswordResetConfirmForm,MyActivationCodeForm
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm, PasswordResetForm, SetPasswordForm
#http://templatecycle.com/tshop/v6/gray/index.html
urlpatterns = [
    path('personalArea/', views.personalArea, name='personalArea'),

    path('register/', views.register, name="register"),
    path('activation_code_form/', views.endreg, name="endreg"),
    # path('',views.activation, name='activation'),
    # path('activate/<key>', views.activation, name="activation"),
    # path('new-activation-link/<user_id>', views.new_activation_link, name="new_activation_link"''),
    # url(r'^activate/(?P<key>.+)$', 'activation'),
    # url(r'^new-activation-link/(?P<user_id>\d+)/$', 'new_activation_link'),

    # path('', include('django.contrib.auth.urls')),
    path(
        'login/',
        views.LoginView.as_view(
            template_name="registration/login.html",
            authentication_form=UserLoginForm
        ),
        name='login'
    ),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name="registration/password_change_form.html", form_class=MyChangePasswordForm,  success_url="/personalArea/"), name='password_change'),
    # path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form.html", form_class=MyPasswordResetForm, from_email="scherbakov@atc-basis.ru"), name='password_reset'),
    path('password_reset/done', auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html", form_class=MyPasswordResetConfirmForm), name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"), name='password_reset_complete'),

]




