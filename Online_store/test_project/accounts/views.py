import hashlib

import datetime
import random
# from .models import Profile
from django.conf import settings
from django.contrib.auth import get_user_model, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.views import View
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from appdirs import unicode
from django.shortcuts import render, redirect, get_object_or_404
# from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage #Импорт пагинатора
from django.urls import reverse_lazy
from django.utils import timezone
from products.models import Product, ProductImage
from orders.models import Order, ProductInOrder, ProductInBasket
# from  django.contrib.auth.forms import UserCreationForm
from .forms import *
# from django.views.generic.edit import FormView
# from django.http import HttpResponseRedirect, HttpResponse
# from django.views.generic.base import View
# from django.contrib.auth import logout
from django.contrib.auth import login
# from django.contrib.auth.forms import AuthenticationForm
# from django.template import RequestContext
from django.contrib.auth.views import LoginView, PasswordContextMixin
from django.contrib.auth import authenticate
# from django.contrib.auth.decorators import login_required
# from django.views.generic import UpdateView
# from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
# from django.urls import reverse_lazy
from django.contrib import messages
import django.contrib.auth.mixins



def personalArea(request):
    # dictOrder = dict()
    # productList = []
    # product_in_orders = ProductInOrder.objects.filter(order__user=request.user)
    # for product in product_in_orders:
    #     productList.append(product.product.name)
    #
    # promegTup = tuple(productList)
    # promegSet = set(promegTup)
    # productList = promegSet

    # for ord in product_in_orders:
    #     dictOrder[ord.order.user] = [ord.order.created, [i for i in ord.product]]
    #
    # dictOrderI = dictOrder.items()

    return render(request, 'accounts/personalArea.html', locals())

# class Signup(View):
#     def get(self, request):
#         form = SignupForm()
#         return render(request, 'registration/register.html', {'form': form})
#
#     def post(self, request):
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             # Create an inactive user with no password:
#             user = form.save(commit=False)
#             user.is_active = False
#             user.set_unusable_password()
#             user.save()
#
#             # Send an email to the user with the token:
#             mail_subject = 'Activate your account.'
#             current_site = get_current_site(request)
#             uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
#             token = account_activation_token.make_token(user)
#             activation_link = "{0}/?uid={1}&token{2}".format(current_site, uid, token)
#             message = "Hello {0},\n {1}".format(user.username, activation_link)
#             to_email = form.cleaned_data.get('email')
#             email = EmailMessage(mail_subject, message, to=[to_email])
#             email.send()
#             return HttpResponse('Please confirm your email address to complete the registration')
#
#         User = get_user_model()
#
# class Activate(View):
#     def get(self, request, uidb64, token):
#         try:
#             uid = force_text(urlsafe_base64_decode(uidb64)).decode()
#             user = User.objects.get(pk=uid)
#         except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#             user = None
#         if user is not None and account_activation_token.check_token(user, token):
#             # activate user and login:
#             user.is_active = True
#             user.save()
#             login(request, user)
#
#             form = PasswordChangeForm(request.user)
#             return render(request, 'activation.html', {'form': form})
#
#         else:
#             return HttpResponse('Activation link is invalid!')
#
#     def post(self, request):
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)  # Important, to update the session with the new password
#             return HttpResponse('Password changed successfully')







#main reg
# def register(request):
#     if not request.user.is_authenticated:
#         if request.POST:
#             form = RegistrationForm(request.POST or None)
#             if form.is_valid():
#                 form.save()
#                 username = form.cleaned_data.get('username')
#                 my_password1 = form.cleaned_data.get('password1')
#
#                 user = authenticate(username=username, password=my_password1)
#                 if user and user.is_active:
#                     login(request, user)
#                     return redirect('/personalArea/')
#                 else:
#                     form.add_error(None, 'Unknown or disabled account')
#                     return render(request, 'registration/register.html', {'form': form})
#                 # my_password2 = form.cleaned_data.get('password2')
#             else:
#                 return render(request, 'registration/register.html', {'form': form})
#         else:
#             return render(request, 'registration/register.html', {'form': RegistrationForm()})
#     else:
#         return redirect('/personalArea/')


# def register(request):
#     if request.user.is_authenticated:
#         return redirect('/personalArea/')
#     registration_form = RegistrationForm()
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             datas={}
#             datas['username'] = form.cleaned_data['username']
#             datas['email'] = form.cleaned_data['email']
#             datas['password1'] = form.cleaned_data['password1']
#             datas['password2'] = form.cleaned_data['password2']
#             datas['firstname'] = form.cleaned_data['firstname']
#
#             #We generate a random activation key
#             salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]
#             usernamesalt = datas['username']
#             if isinstance(usernamesalt, unicode):
#                 usernamesalt = usernamesalt.encode('utf-8')
#             datas['activation_key']= hashlib.sha1(str(salt).encode('utf-8')+usernamesalt).hexdigest()
#
#
#             datas['email_subject']="Activation de votre compte yourdomain"
#
#             form.sendEmail(datas)
#             form.save(datas) #Save the user and his profile
#
#             request.session['registered']=True #For display purposes
#             return redirect('/personalArea/')
#         else:
#             registration_form = form #Display form with error messages (incorrect fields, etc)
#     return render(request, "registration/register.html", locals())
#
#
# def activation(request, key):
#     activation_expired = False
#     already_active = False
#     profile = get_object_or_404(Profile, activation_key=key)
#     if profile.user.is_active == False:
#         if timezone.now() > profile.key_expires:
#             activation_expired = True #Display: offer the user to send a new activation link
#             id_user = profile.user.id
#         else: #Activation successful
#             profile.user.is_active = True
#             profile.user.save()
#
#     #If user is already active, simply display error message
#     else:
#         already_active = True #Display : error message
#     return render(request, 'registration/password_reset_done.html.html', locals())
#
#
#
#
# def new_activation_link(request, user_id):
#     form = RegistrationForm()
#     datas={}
#     user = User.objects.get(id=user_id)
#     if user is not None and not user.is_active:
#         datas['username']=user.username
#         datas['email']=user.email
#         # datas['email_path']="/ResendEmail.txt"
#         datas['email_subject']="Nouveau lien d'activation yourdomain"
#
#         salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]
#         usernamesalt = datas['username']
#         if isinstance(usernamesalt, unicode):
#             usernamesalt = usernamesalt.encode('utf8')
#         datas['activation_key']= hashlib.sha1(str(salt).encode('utf-8')+usernamesalt).hexdigest()
#
#         profile = Profile.objects.get(user=user)
#         profile.activation_key = datas['activation_key']
#         profile.key_expires = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=2), "%Y-%m-%d %H:%M:%S")
#         profile.save()
#
#         form.sendEmail(datas)
#         request.session['new_link']=True #Display: new link sent
#
#     return redirect('/personalArea/')
#
#
# def generate_activation_key(username):
#     chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
#     secret_key = get_random_string(20, chars)
#     return hashlib.sha256((secret_key + username).encode('utf-8')).hexdigest()

def generate_code():
    random.seed()
    return str(random.randint(10000,99999))

def register(request):
    if not request.user.is_authenticated:
        if request.POST:
            form = RegistrationForm(request.POST or None)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                email = form.cleaned_data.get('email')
                my_password1 = form.cleaned_data.get('password1')
                # u_f = User.objects.get(username=username, email=email, is_active=False)
                code = generate_code()
                request.session["code"] = code
                request.session["username"] = username
                # if Profile.objects.filter(code=code):
                #     # for p in Profile.objects.filter(code=code):
                #     #     p.delete()
                #     code = generate_code()

                message = code
                user = authenticate(username=username, password=my_password1)
                now = datetime.datetime.now()

                # Profile.objects.create(user=u_f, code=code, date=now)

                send_mail('код подтверждения', message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False)
                if user and user.is_active:
                    login(request, user)
                    return redirect('/personalArea/')
                else: #тут добавить редирект на страницу с формой для ввода кода.
                    # form.add_error(None, 'Аккаунт не активирован')
                    return redirect('/activation_code_form/')
                    # return render(request, 'registration/register.html', {'form': form})
            else:
                return render(request, 'registration/register.html', {'form': form})
        else:
            return render(request, 'registration/register.html', {'form':
            RegistrationForm()})
    else:
        return redirect('/personalArea/')

def endreg(request):
    if  request.user.is_authenticated:
        return redirect('/personalArea/')
    else:
        if request.method == 'POST':
            form = MyActivationCodeForm(request.POST)
            if form.is_valid():
                code_use = form.cleaned_data.get("code")
                code_session = request.session.get("code", " ")
                user_session = request.session.get("username", " ")
                user = User.objects.get(username=user_session)
                if code_use == code_session:
                    if user.is_active == False:
                        user.is_active = True
                        user.save()
                        login(request, user)

                        return redirect('/personalArea/')
                    else:
                        form.add_error(None, 'Аккаунт уже активирован.')
                        return render(request, 'registration/activation_code_form.html', {'form': form})

                else:
                    form.add_error(None, 'Код подтверждения не совпадает.')
                    return render(request, 'registration/activation_code_form.html', {'form': form})
                # if Profile.objects.filter(code=code_use):
                #     profile = Profile.objects.get(code=code_use)
                # else:
                #     form.add_error(None, "Код подтверждения не совпадает.")
                #     return render(request, 'registration/activation_code_form.html', {'form': form})
                # if profile.user.is_active == False:
                #     profile.user.is_active = True
                #     profile.user.save()
                #     # user = authenticate(username=profile.user.username, password=profile.user.password)
                #     login(request, profile.user)
                #     profile.delete()
                #     return redirect('/personalArea/')

            else:
                return render(request, 'registration/activation_code_form.html', {'form': form})
        else:
            form = MyActivationCodeForm()
            return render(request, 'registration/activation_code_form.html', {'form': form})



# def activation(request):
#     # profile = get_object_or_404(Profile, co=key)
#     profile = Profile.objects.filter(is_active=False)
#     now = datetime.datetime.now() + datetime.timedelta(days=2)
#     for p in profile:
#         if now > p.date:
#             p.delete()
#     return render(request, 'landing/home.html', locals())


def password_reset_confirm(request):
    if not request.user.is_authenticated:
        return redirect('/personalArea/')


# def UpdatePassword(request):
#     form = PasswordChangeForm(user=request.user)
#
#     if request.method == 'POST':
#         form = PasswordChangeForm(user=request.user, data=request.POST)
#         if form.is_valid():
#             form.save()
#             update_session_auth_hash(request, form.user)
#
#     return render(request, 'registration/password_change_form.html', {
#         'form': form,
#     })




# def password_change(request):
#     if request.method == 'POST':
#         form = MyChangePasswordForm(data=request.POST, user=request.user)
#         if form.is_valid():
#             form.save()
#             current_password = request.user.password
#             new_password1 = request.POST.get('new_password1')
#             if current_password != new_password1:
#                 update_session_auth_hash(request, form.user)
#                 messages.success(request, 'Your password was successfully updated!')
#                 return redirect('/personalArea/')
#             else:
#                 return render(request, 'registration/password_change_form.html', {'form': form})
#         else:
#             return render(request, 'registration/password_change_form.html', {'form': form})
#     else:
#         return render(request, "registration/password_change_form.html", {'form': MyChangePasswordForm()})
