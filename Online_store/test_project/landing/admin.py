from django.contrib import admin
from .models import *
# class SubscriberAdmin(admin.ModelAdmin):
#     #list_display = ['name', 'email']  #Показывает какие поля мы хотим выводить
#     list_display = [field.name for field in Subscriber._meta.fields]#Subscriber._meta.fields- получает все поля; В итоге выводит все поля в модели
#     #exclude = ["email"] # Исключает поля из редактирования записи
#     list_filter = ["name",]#Добавляет справо колонку фильтра, по введеному полю
#     search_fields = ["name", "email"]#Добавляет строку поиска по полю/полям
#     fields = ["email"] # Обраное exclude, в полях какие есть выводит только это значение
#
#     class Meta:
#         model = Subscriber
#
#
# admin.site.register(Subscriber, SubscriberAdmin) #SubscriberAdmin перезапишет Subscriber модель с другими настройками
#

