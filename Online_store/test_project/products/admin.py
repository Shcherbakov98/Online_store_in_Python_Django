from django.contrib import admin
from .models import *

class ProductImageInline(admin.TabularInline):  #Добавляет в товары к одному товару все фото связанные с ним
    model = ProductImage
    extra = 0 #Добавленные по умолчанию фото


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductCategory._meta.fields]
    class Meta:
        model = ProductCategory
admin.site.register(ProductCategory, ProductCategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.fields]
    exclude = ["str_price", "str_discount_price"] # Исключает поля из редактирования записи
    list_filter = ['name']
    search_fields = ['name']
    inlines = [ProductImageInline]
    class Meta:
        model = Product

admin.site.register(Product, ProductAdmin)

class ProductImageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductImage._meta.fields]

    class Meta:
        model = ProductImage

admin.site.register(ProductImage, ProductImageAdmin)
