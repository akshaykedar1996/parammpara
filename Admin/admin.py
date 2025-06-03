from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(AdminDT)
class ProductAdmin(admin.ModelAdmin):
   
    list_display = [field.name for field in AdminDT._meta.fields]   