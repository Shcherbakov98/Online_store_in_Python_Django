from django.shortcuts import render
# from .forms import  SubscriberForm
from products.models import ProductImage, Product

# def landing(request):
#     name = 'Artem'
#     current_day = '13.03.2020'
#     form = SubscriberForm(request.POST or None)
#     session_key = request.session.session_key
#     if not session_key:  # Ключ сессии , если пользователь не авторизирован
#         request.session.cycle_key()
#
#     if request.method == "POST" and form.is_valid():
#         print(request.POST)
#         print(form.cleaned_data)
#         data = form.cleaned_data
#         print(form.cleaned_data["name"])
#         print(data["name"])
#         new_form = form.save()
#
#     return render(request, 'landing/landing.html', locals())

def home(request):
    products_images = ProductImage.objects.filter(is_active=True, is_main=True, product__is_active=True)
    # products_images_phones = products_images.filter(product__category__id=1)#В кверисетах обращение по полю через __
    # products_images_laptops = products_images.filter(product__category__id=2)
    products_image_new = products_images.order_by('-product__created')[0:4] #Новые постувпления по дате
    products_image_hits = products_images.order_by('-product__price')[0:4]
    products = Product.objects.all()
    return render(request, 'landing/home.html', locals())

def phones(request):
    products_images = ProductImage.objects.filter(is_active=True, is_main=True, product__is_active=True)
    products_images_phones = products_images.filter(product__category__id=1)
    return render(request, 'landing/phones.html', locals())

def laptops(request):
    products_images = ProductImage.objects.filter(is_active=True, is_main=True, product__is_active=True)
    products_images_laptops = products_images.filter(product__category__id=2)
    return render(request, 'landing/laptops.html', locals())
# def product(request, product_id):
#     product = Product.objects.get(id=product_id)
#     session_key = request.session.session_key
#     if not session_key:  #Ключ сессии , если пользователь не авторизирован
#         request.session.cycle_key()
#     print(request.session.session_key) #Уникальный идентификатор сессии , для работы с корзиной
#
#     return render(request, 'landing/home.html', locals())