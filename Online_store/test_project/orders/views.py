from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from .models import *
from django.shortcuts import render
from django.contrib.auth.models import User
from .forms import CheckoutContactForm
from products.models import ProductImage
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate


def basket_adding(request):
    return_dict = dict()
    session_key = request.session.session_key
    print (request.POST)
    data = request.POST
    product_id = data.get("product_id")
    nmb = data.get("nmb")
    is_delete = data.get("is_delete")
    if is_delete == 'true':
        if request.user.is_authenticated:
            ProductInBasket.objects.filter(user=request.user, product__id=product_id).update(is_active=False)
        else:
            ProductInBasket.objects.filter(session_key=session_key, product__id=product_id).update(is_active=False)
    else:
        if request.user.is_authenticated:
            new_product, created = ProductInBasket.objects.get_or_create(user=request.user, product_id=product_id, is_active=True, defaults={"nmb": nmb})
        else:
            new_product, created = ProductInBasket.objects.get_or_create(session_key=session_key, product_id=product_id, is_active=True, defaults={"nmb": nmb})


        if not created:
            print ("not created")
            new_product.nmb += int(nmb)
            new_product.save(force_update=True)

    #common code for 2 cases
    if request.user.is_authenticated:
        products_in_basket = ProductInBasket.objects.filter(user=request.user, is_active=True)
    else:
        products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True)
    products_total_nmb = products_in_basket.count()
    return_dict["products_total_nmb"] = products_total_nmb
    return_dict["products"] = list()
    for item in  products_in_basket:
        product_dict = dict()
        product_dict["id"] = item.product.id
        product_dict["name"] = item.product.name
        if item.product.discount:
            product_dict["price_per_item"] = item.product.str_discount_price
        else:
            product_dict["price_per_item"] = item.product.str_price
        product_dict["nmb"] = item.nmb
        return_dict["products"].append(product_dict)

    return JsonResponse(return_dict)

def checkout(request):
    session_key = request.session.session_key
    if request.user.is_authenticated:
        products_in_basket = ProductInBasket.objects.filter(user=request.user, is_active=True)
    else:
        products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True)

    print (products_in_basket)
    for item in products_in_basket:
        print(item.order)
    form = CheckoutContactForm(request.POST or None)
    if request.POST:
        print(request.POST)
        if form.is_valid() or request.user.is_authenticated:
            if not request.user.is_authenticated:
                print("yes")
                data = request.POST
                name = data.get("name",)
                phone = data["phone"]
                email = data["email"]
                address = data["address"]
                comments = data["comments"]
            else:
                data = request.POST
                address = data["address"]
                comments = data["comments"]
            if request.user.is_authenticated:
                user = request.user
                order = Order.objects.create(user=user, customer_phone=request.user.first_name, customer_email=request.user.email, customer_address=address, comments=comments, status_id=1)
            else:
                user, created = User.objects.get_or_create(username=name,email=email, first_name=phone)
                order = Order.objects.create(user=user, customer_phone=phone, customer_email=email, customer_address=address, comments=comments, status_id=1)
            for name, value in data.items():
                if name.startswith("product_in_basket_"):
                    product_in_basket_id = name.split("product_in_basket_")[1]
                    product_in_basket = ProductInBasket.objects.get(id=product_in_basket_id)
                    print(type(value))
                    product_in_basket.nmb = value
                    product_in_basket.order = order
                    products_in_basket.is_active=False
                    product_in_basket.save(force_update=True)

                    ProductInOrder.objects.create(product=product_in_basket.product, nmb = product_in_basket.nmb,
                                                  price_per_item=product_in_basket.price_per_item,
                                                  total_price = product_in_basket.total_price,
                                                  order=order)

            if request.user.is_authenticated:
                username = request.user.username
                my_password1 = request.user.password
                ProductInBasket.objects.filter(user=request.user).delete()
            else:
                request.session.flush()
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            print("no")
    return render(request, 'orders/checkout.html', locals())

