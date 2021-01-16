from django.db import models

# class Subscriber(models.Model):
#     email = models.EmailField()
#     name = models.CharField(max_length=128)
#
#     def __str__(self): # Вызывается запись из этой модели, для каждой записи возвращается введеное поле и отражается в admin
#         return "Пользователь: %s Email: %s" % (self.name, self.email) #str_(self) - метод, вызываемый функциями str, print и format. Возвращает строковое представление объекта.
#
#     class Meta:
#         verbose_name = "MySubscriber" #Меняет название таблицы внутри
#         verbose_name_plural = "A lot of Subscribers" # Меняет название таблицы снаружи для множественного числа
#
#
