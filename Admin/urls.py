from django.urls import path
from .views import *
from . import views
urlpatterns = [  
    
    path('', login_admin , name='login_admin' ),
    path('logout-admin/', views.logout_admin, name='logout_admin'),
    path('home/', home , name='super_index' ),

    # carousel
    path('carousel/', views.carousel_list, name='carousel_list'),
    path('carousel/add/', views.carousel_add, name='carousel_add'),
    path('carousel/edit/<int:pk>/', views.carousel_edit, name='carousel_edit'),
    path('carousel/delete/<int:pk>/', views.carousel_delete, name='carousel_delete'),

    # MainService
    path('mainservices/', views.mainservice_list, name='mainservice_list'),
    path('mainservices/add/', views.mainservice_add, name='mainservice_add'),
    path('mainservices/edit/<int:pk>/', views.mainservice_edit, name='mainservice_edit'),
    path('mainservices/delete/<int:pk>/', views.mainservice_delete, name='mainservice_delete'),

    # SubService
    path('subservices/', views.subservice_list, name='subservice_list'),
    path('subservices/add/', views.subservice_add, name='subservice_add'),
    path('subservices/edit/<int:pk>/', views.subservice_edit, name='subservice_edit'),
    path('subservices/delete/<int:pk>/', views.subservice_delete, name='subservice_delete'),

    # testimonials#
    path('testimonials/', views.testimonials_list, name='testimonials_list'),
    path('testimonials/add/', views.add_testimonial, name='add_testimonial'),
    path('testimonials/edit/<int:pk>/', views.edit_testimonial, name='edit_testimonial'),
    path('testimonials/delete/<int:pk>/', views.delete_testimonial, name='delete_testimonial'),

    path('franchise_list/', views.Franchise_list, name='Franchise_list'),
    path('appointments/toggle-status/<int:pk>/', views.toggle_appointment_status, name='toggle_appointment_status'),
    

    path('contacts/', views.contact_list, name='contact_list'),
    path('contacts/toggle-status/<int:pk>/', views.toggle_contact_status, name='toggle_contact_status'),

    path('product-list', views.product_list, name='product_list'),
    path('create/', views.product_create, name='product_create'),
    path('<uuid:pk>/edit/', views.product_update, name='product_update'),
    path('<uuid:pk>/delete/', views.product_delete, name='product_delete'),


    path('pd/categories/', views.category_list, name='category_list'),
    path('pd/categories/add/', views.category_create, name='product_category_create'),
    path('pd/categories/<int:pk>/edit/', views.category_update, name='category_update'),
    path('pd/categories/<int:pk>/delete/', views.category_delete, name='category_delete'),

    path('product-dt/<str:Product_id>/', views.product_detail, name='admin_product-detail'),

    # SubCategory URLs
    path('pd/subcategories/', views.subcategory_list, name='subcategory_list'),
    path('pd/subcategories/add/', views.subcategory_create, name='subcategory_create'),
    path('pd/subcategories/<int:pk>/edit/', views.subcategory_update, name='subcategory_update'),
    path('pd/subcategories/<int:pk>/delete/', views.subcategory_delete, name='subcategory_delete'),

    path('orders/', views.orders, name='orders'),
    path('invoice/<str:order_id>/', views.order_invoice, name='order-invoice'),

    path('update_order_status/', update_order_status, name='update_order_status'),
    path('orders/<str:status>/', admin_all_order_by_status, name='admin_order_by_status'),


    path('franchise-services/', Franchiseservice_list, name='Franchiseservice_list'),
    path('franchise-services/add/', Franchiseservice_add, name='Franchiseservice_add'),
    path('franchise-services/edit/<int:pk>/', Franchiseservice_edit, name='Franchiseservice_edit'),
    path('franchise-services/delete/<int:pk>/', Franchiseservice_delete, name='Franchiseservice_delete'),  
]
