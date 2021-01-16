from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage #Импорт пагинатора
from products.models import Product, ProductImage

def search(request):
    products = Product.objects.all()
    DictName = {}
    itog = []
    for product in products:
        DictName[product.name] = (product.name + " " +  str(product.id)).split()
    print(DictName)
    if request.POST:
        print(request.POST)
        data = request.POST
        q = data["q"].lower()
        print(q)
        for k,v in DictName.items():
            if q == k.lower():
                itog.append((k, v[-1]))
                continue
            for z in v:
                if q == z.lower() and z != v[-1]:
                    itog.append((k, v[-1]))
    setDict = set(itog)
    print(itog)
    products_images = []
    for p, id in setDict:
        products_images_object = ProductImage.objects.filter(is_active=True, is_main=True, product__is_active=True, product__id=id)
        products_images.append(products_images_object)


    return render(request, 'searchProduct/search.html', locals())

