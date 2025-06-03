from django.urls import path
from .views import *
urlpatterns = [
    path('login/', login_user , name='login_user'),
    path('log-out/', logout_user , name='logout_user'),
    path('forgot-password/', forgot_password , name='forgot_password'),

    path('forgot-password/', forgot_password, name='forgot_password'),
    path('verify-otp/', verify_otp, name='verify_otp'),
  

    path('regiter/', user_register , name='regiter'),
    path('code/verify/', register_verify, name="register_verify"),

    path('accounts/google/login/', google_login, name='google_login'),
    path('accounts/google/callback/', google_callback, name='google_callback_login'),

    path('load-navbar-data/', load_navbar_data, name='load_navbar_data'),
    path('ecoomerc/home/', ecoomerc_home , name='ecoomerc_home'),

    path('profile/', profile , name='profile'),
    # urls.py
    
    path('products/', all_products , name='all_products'),
    path('category/<str:name>/', category_filter, name='category-filter'),
    path('sub-category/<str:name>/', sub_category_filter, name='sub-category-filter'),
    path('product-dt/<str:Product_id>/', product_detail, name='product-detail'),
    path('add-to-cart/', add_to_cart, name='add_to_cart'),
    path('checkout/', checkout, name='checkout'),
    path('Cart-dt/', Cart_dt, name='Cart-dt'),
    path('update_cart/', update_cart, name='update_cart'),
    path('remove_cart/', remove_cart, name='remove_cart'),
    path('Check-out/', Check_out, name='Check_out'),

    path('orders/', user_all_order, name='user_all_order'),
    path('orders/<str:status>/', user_all_order_by_status, name='user_order_by_status'),
]
