from django.db import models

class ProductCategory(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категория товаров'



class Product(models.Model): #Продукт
    name = models.CharField(max_length=64, blank=True, null=True, default=None)
    price = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    price_discount = models.IntegerField(default=0)
    str_price = models.TextField(blank=True, null=True, default=None)
    str_discount_price = models.TextField(blank=True, null=True, default=None)
    category = models.ForeignKey(ProductCategory, blank=True, null=True, default=None, on_delete=models.CASCADE)
    specifications = models.TextField(blank=True, null=True, default=None)  # Описание
    description = models.TextField(blank=True, null=True, default=None)#Описание
    is_active = models.BooleanField(default=True)  # Скрывать или показывать продукт
    created = models.DateTimeField(auto_now_add=True, auto_now=False) #Значение записывается автоматически , когда создается запись в Product
    update = models.DateTimeField(auto_now_add=False, auto_now=True) #Значение будет автоматически имзенено, когда делается любой update записи модели в Product


    def __str__(self):
        return "%s, %s₽" % (self.name, self.price)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def save(self, *args, **kwargs):
        d = self.discount
        p = self.price
        if int(d) > 0:
            per =  p * d / 100
            itog = p - int(per)
            self.price_discount = itog
        price = self.price
        disc = self.price_discount
        firstCharP = price // 1000
        secondCharP = price % 1000
        if secondCharP == 0:
            secondCharP = '000'
        firstCharD = disc // 1000
        secondCharD = disc % 1000
        if secondCharD == 0:
            secondCharD = '000'
        self.str_discount_price = str(firstCharD) + " " + str(secondCharD)
        self.str_price = str(firstCharP) + " " + str(secondCharP)
        super(Product, self).save(*args, **kwargs)

class ProductImage(models.Model):#Фото продукта
    product = models.ForeignKey(Product, blank=True, null=True, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products_images', blank=True) #upload_to= показывает куда надо картинку загружать относительно папки media
    is_main = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)#Скрывать или показывать фото
    created = models.DateTimeField(auto_now_add=True, auto_now=False) #Значение записывается автоматически , когда создается запись в Order
    update = models.DateTimeField(auto_now_add=False, auto_now=True) #Значение будет автоматически имзенено, когда делается любой update записи модели в Order
    #@property возвращает ссылку на фото когда мы обращаемся  к полю
    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'