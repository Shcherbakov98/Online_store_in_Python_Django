from django.db import models
from products.models import Product, ProductImage
from django.db.models.signals import post_save
from django.contrib.auth.models import User

#null = True устанавливает NULL (вместо NOT NULL) для столбца в вашей БД. Пустые значения для типов полей Django, таких как DateTimeField или ForeignKey, будут сохранены как NULL в БД.
#blank определяет, будет ли поле заполнено в формах. Это включает в себя администратора и ваши пользовательские формы. Если blank = True, то поле не будет обязательным, тогда как если False, поле не может быть пустым.

class Status(models.Model):
    name = models.CharField(max_length=24, blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False) #Значение записывается автоматически , когда создается запись в Order
    update = models.DateTimeField(auto_now_add=False, auto_now=True) #Значение будет автоматически имзенено, когда делается любой update записи модели в Order


    def __str__(self):
        return "Статус %s" % self.name

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы заказа'


class Order(models.Model): #Заказ
    user = models.ForeignKey(User, blank=True, null=True, default=None, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10,decimal_places=2,default=0)  # цкна для всех товаров в заказе
    # customer_name = models.CharField(max_length=64, blank=True, null=True, default=None)
    customer_email = models.EmailField(blank=True, null=True, default=None)
    customer_phone = models.CharField(max_length=48, blank=True, null=True, default=None)
    customer_address = models.CharField(max_length=128, blank=True, null=True, default=None)
    comments = models.TextField(blank=True, null=True, default=None)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, auto_now=False) #Значение записывается автоматически , когда создается запись в Order
    update = models.DateTimeField(auto_now_add=False, auto_now=True) #Значение будет автоматически имзенено, когда делается любой update записи модели в Order
    def __str__(self):
        return "Заказ %s %s %s" % (self.id, self.status.name, self.user)
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)

#Для создания рекурсивной связи – объект со связью многое-к-одному на себя – используйте models.ForeignKey('self', on_delete=models.CASCADE).
class ProductInOrder(models.Model): #товар
    order = models.ForeignKey(Order, blank=True, null=True, default=None, on_delete=models.CASCADE)#Ссылка на заказ
    product = models.ForeignKey(Product, blank=True, null=True, default=None, on_delete=models.CASCADE)  # Ссылка на продукт
    nmb = models.IntegerField(default=1) #kol-vo
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0) # Цена фиксирует по какой цене был продан товар
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0) #price * nmb общая стоимость
    is_active = models.BooleanField(default=True)  # Скрывать или показывать товар
    created = models.DateTimeField(auto_now_add=True, auto_now=False) #Значение записывается автоматически , когда создается запись в Order
    update = models.DateTimeField(auto_now_add=False, auto_now=True) #Значение будет автоматически имзенено, когда делается любой update записи модели в Order


    def __str__(self):
        return "%s" % self.product.name

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'
#Метод переопределения для подсчета логики товаров в запасе в базе данных
    def save(self, *args, **kwargs):
        price_per_item = self.product.price #Узнает цену товара
        self.price_per_item = price_per_item #присваевает в табл pinord значение цены товара за единицу
        self.total_price =  int(self.nmb) * price_per_item # записывает в общую цену количество товаров умнож на цену
        super(ProductInOrder, self).save(*args, **kwargs)

def product_in_order_post_save(sender, instance, created,  **kwargs):
    order = instance.order  # 3aka3
    all_products_in_order = ProductInOrder.objects.filter(order=order, is_active=True)  # Подсчет всех заказов в заказе
                                                                                      #order=order - в фильтре кверисета это означает, что мы выбираем все записи, в которых поле order равняется переменной order, а переменная order определена чуть выше этого кверисета
    order_total_price = 0
    for item in all_products_in_order:  # Проходимся по всем ценам и записываем в тотал прайс заказа
        order_total_price += item.total_price
    instance.order.total_price = order_total_price
    instance.order.save(force_update=True)  # Обновить текущую запись при сохранении

post_save.connect(product_in_order_post_save, sender=ProductInOrder) #вызываем post_save присоединяем функцию выше, указываем отправителя


class ProductInBasket(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, default=None, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=128, blank=True, null=True, default=None)
    order = models.ForeignKey(Order, blank=True, null=True, default=None, on_delete=models.CASCADE)#Ссылка на заказ
    product = models.ForeignKey(Product, blank=True, null=True, default=None, on_delete=models.CASCADE)  # Ссылка на продукт
    nmb = models.IntegerField(default=1) #kol-vo
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0) # Цена фиксирует по какой цене был продан товар
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0) #price * nmb общая стоимость
    is_active = models.BooleanField(default=True)  # Скрывать или показывать товар
    created = models.DateTimeField(auto_now_add=True, auto_now=False) #Значение записывается автоматически , когда создается запись в Order
    update = models.DateTimeField(auto_now_add=False, auto_now=True) #Значение будет автоматически имзенено, когда делается любой update записи модели в Order

    def __str__(self):
        return "%s" % self.product.name

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def save(self, *args, **kwargs):
        price_per_item = self.product.price  # Узнает цену товара
        price_per_item_discount = self.product.price_discount
        if self.product.discount:
            self.price_per_item = price_per_item_discount
            self.total_price = int(self.nmb) * price_per_item_discount
        else:
            self.price_per_item = price_per_item
            self.total_price = int(self.nmb) * price_per_item
        super(ProductInBasket, self).save(*args, **kwargs)