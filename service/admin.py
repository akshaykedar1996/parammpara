from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CarouselImage 

admin.site.register(CarouselImage)


from django.contrib import admin
from .models import *

class SubServiceInline(admin.TabularInline):
    model = SubService
    extra = 1

@admin.register(MainService)
class MainServiceAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = [SubServiceInline]

@admin.register(SubService)
class SubServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'main_service')
    search_fields = ('title', 'main_service__title')


admin.site.register(Testimonials)


admin.site.register(Contact)


@admin.register(Franchiseservice)
class FranchiseserviceAdmin(admin.ModelAdmin):
    list_display = ('img1', 'title','paragraph','description','img2')
    search_fields = ('img1', 'title','paragraph','description','img2')
    


@admin.register(Franchise)
class FranchiseAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_no','email','date','time','address','status')
    search_fields = ('name', 'contact_no','email','date','time','address','status')    
    
 
    
    

