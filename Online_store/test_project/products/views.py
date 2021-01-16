from django.shortcuts import render
from products.models import Product

def product(request, product_id):
    product = Product.objects.get(id=product_id)
#Работа с характеристиками продукта
    myDict = dict()
    fout = open("output.txt", "w", encoding="utf8")
    print(product.specifications, file=fout)
    fout.close()
    fin = open("output.txt", "r", encoding="utf8")
    for line in fin:
        ft = line.find("-")
        if line[:ft].strip() == "" and line[ft + 1:].strip() == "":
            continue
        myDict[line[:ft].strip()] = line[ft + 1:].strip()
    # print(myDict)
    myDictS = myDict.items()
    fin.close()
#Работа с "О продукте"
    myListProduct = []
    fout = open("output.txt", "w", encoding="utf8")
    print(product.description, file=fout)
    fout.close()
    fin = open("output.txt", "r", encoding="utf8")
    for line in fin:
        myListProduct.append(line.strip())
    fin.close()


    session_key = request.session.session_key
    if not session_key:  #Ключ сессии , если пользователь не авторизирован
        request.session.cycle_key()
    print(request.session.session_key) #Уникальный идентификатор сессии , для работы с корзиной

    return render(request, 'products/product.html', locals())


