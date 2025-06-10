from django.urls import path
from .views import *
urlpatterns = [

    path('', home , name='index'),
    path('services/', service , name='service'),
    path('services/<int:service_id>/', service_detail_view, name='service_detail'),
    path('sub-service/<int:id>/', sub_service_detail, name='sub_service_detail'),
    path('abouts/', abouts , name='about'),

    path('contact-us/', Contact_us, name='contact_us'),
    path('franchise/', franchise, name='franchise'),
    
    path('privacy_policy/', privacy_policy, name='privacy_policy'),
    path('terms_of_service/', terms_of_service, name='terms_of_service'),
    
    
    path('add-service/', add_services, name='add_service'),
    path('edit-service/', edit_services, name='edit_service'),
    path('all-services/', services_list, name='all_services'),
    path('services/', services_page, name='services_page'),
    path('read-more/<int:service_id>/', read_more_view, name='read_more'),
    
]
