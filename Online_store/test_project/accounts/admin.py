from django.contrib import admin
# from .models import Profile
from django.contrib.auth.models import User


# class ProfileInline(admin.TabularInline):  #присоединил  к заказу, продукт который был заказан
#     model = User
#     extra = 0 #Добавленные по умолчанию



# class ProfileAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in Profile._meta.fields]
#     class Meta:
#         model = Profile
# admin.site.register(Profile, ProfileAdmin)

