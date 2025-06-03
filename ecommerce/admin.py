from django.contrib import admin

# Register your models here.
from .models import *
# Register your models here.
@admin.register(Ecommerc_User)
class ProductAdmin(admin.ModelAdmin):
   
    list_display = [field.name for field in Ecommerc_User._meta.fields]   

@admin.register(Category)
class ProductAdmin(admin.ModelAdmin):
   
    list_display = [field.name for field in Category._meta.fields]   

@admin.register(SubCategory)
class ProductAdmin(admin.ModelAdmin):
   
    list_display = [field.name for field in SubCategory._meta.fields]   

@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
   
    list_display = [field.name for field in Products._meta.fields]       


@admin.register(Cart)
class ProductAdmin(admin.ModelAdmin):
   
    list_display = [field.name for field in Cart._meta.fields]     


@admin.register(Order)
class ProductAdmin(admin.ModelAdmin):
   
    list_display = [field.name for field in Order._meta.fields]         