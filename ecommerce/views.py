
from django.shortcuts import render , HttpResponse , redirect
from .models import *
from django.conf import settings
import requests as r
from django.core.mail import send_mail
from django.utils.crypto import get_random_string

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
import uuid
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

'''
=====================================================================================================================================
                                                       Login out user method 
=====================================================================================================================================
'''

def logout_user(request):
    if 'user_uid' not in request.session:
        return redirect(f"/login/?next={request.get_full_path()}")
    user_id = request.session.get('user_uid')
    del request.session['user_uid']
    return redirect('login_user')


from django.contrib import messages

'''
=====================================================================================================================================
                                                       Login user method 
=====================================================================================================================================
'''

@csrf_exempt
def login_user(request):
    if request.session.get('user_uid'):
        return redirect('ecoomerc_home')  
    
    next_url = request.GET.get('next', 'ecoomerc_home')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        try:
            user = Ecommerc_User.objects.get(email=email)
            if password == user.password:
                if user.status == False:
                    messages.error(request, 'User Not Verify try to forgot paasword?')  # 👈 Error Message
                    return render(request, 'e_commerc/login.html')
                
                request.session['user_uid'] = user.user_uid
                if remember_me:
                    request.session.set_expiry(2592000)  # 30 days in seconds
                else:
                    request.session.set_expiry(0)
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid password.')  # 👈 Error Message
                return render(request, 'e_commerc/login.html')
        except Ecommerc_User.DoesNotExist:
            messages.error(request, 'User not found.')  # 👈 Error Message
            return render(request, 'e_commerc/login.html')

    return render(request, 'e_commerc/login.html')


'''
=====================================================================================================================================
                                                       Login with google method 
=====================================================================================================================================
'''


def google_login(request):
    # Check if 'state' parameter is passed, otherwise default to 'login'
    state = request.GET.get('state', 'login')  # 'login' default state

    google_auth_url = (
        'https://accounts.google.com/o/oauth2/v2/auth'
        f'?response_type=code'
        f'&client_id={settings.GOOGLE_CLIENT_ID}'
        f'&redirect_uri={settings.GOOGLE_REDIRECT_URI_LOGIN}'
        f'&scope=profile email'
        f'&access_type=offline'
        f'&state={state}'  # Pass state parameter here
    )
    return redirect(google_auth_url)

import random
import string
import requests

def google_callback(request):
    code = request.GET.get('code')
    state = request.GET.get('state', 'login')  # Default to 'login' if state is not provided

    if not code:
        messages.error(request, 'Authorization code not received')
        return redirect('/cpanel/login/?msg=Authorization code not received')

    # Authorization code ko tokens mein convert karna
    token_url = 'https://oauth2.googleapis.com/token'
    token_data = {
        'code': code,
        'client_id': settings.GOOGLE_CLIENT_ID,
        'client_secret': settings.GOOGLE_CLIENT_SECRET,
        'redirect_uri': settings.GOOGLE_REDIRECT_URI_LOGIN,
        'grant_type': 'authorization_code',
    }
    token_r = requests.post(token_url, data=token_data)
    token_info = token_r.json()
    access_token = token_info.get('access_token')

    if not access_token:
        messages.error(request, 'Failed to get access token')
        return redirect(f"/login/?next={request.get_full_path()}")

    # User information fetch karna
    user_info_url = 'https://www.googleapis.com/oauth2/v2/userinfo'
    user_info_params = {'access_token': access_token}
    user_info_r = requests.get(user_info_url, params=user_info_params)
    user_info = user_info_r.json()
    email = user_info.get('email')
    name = user_info.get('name')

    if not email:
        messages.error(request, 'Failed to get user info')
        return redirect(f"/login/?next={request.get_full_path()}")

    if state == 'register':
        # User registration handle karna
       
        user, created = Ecommerc_User.objects.get_or_create(email=email, defaults={
            'name': name,
            # 'google_user_id': user_info.get('id'),
            'status': True,
          
        })
        try:
            if created:
                pp = generate_random_password(length=6) 
                user.password = pp
                user.save()
                subject = 'Hello name'
                message = f'Your Email: {email} and password :( {pp} ) URL https://new.joytilingtechnology.com/ecoomerc/home/'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email]  # Add recipient email addresses here
                send_mail(subject, message, email_from, recipient_list)
                messages.success(request, 'User registered successfully')
            else:
                messages.info(request, 'User already exists')
        except:
            pass        

    elif state == 'login':
        # User login handle karna
        try:
            user = Ecommerc_User.objects.get(email=email)
          #  auth_login(request, user)
            messages.info(request, 'User logged in successfully')
        except Ecommerc_User.DoesNotExist:
            user, created = Ecommerc_User.objects.get_or_create(email=email, defaults={
            'name': name,
            # 'google_user_id': user_info.get('id'),
            'status': True,
            })
            return redirect(f"/login/?next={request.get_full_path()}")

    else:
        messages.error(request, 'Invalid state parameter')
        return redirect(f"/login/?next={request.get_full_path()}")

    # User ko session mein set karna
    request.session['user_uid'] = user.user_uid
  #  request.session.set_expiry(172800)  # 30 days in seconds
    return redirect(f"/login/?next={request.get_full_path()}")

def generate_random_password(length=6):

    digits = string.digits  # This contains '0123456789'
    return ''.join(random.choice(digits) for _ in range(length))


'''
=====================================================================================================================================
                                                       user_register method 
=====================================================================================================================================
'''

import uuid

def user_register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone_number')
        password = request.POST.get('password')
    

        if Ecommerc_User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('user_login')
        
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])    
        user = Ecommerc_User(
            # user_uid=uuid.uuid4().hex[:8],
            name=name,
            email=email,
            phone_number=phone,
            password=password,  # Optional: use make_password(password) for security
            verify_code = code
        )
        subject = 'Hello send verify code!'
        message = f'Verification code is .{code}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]  # Add recipient email addresses here
        try:
            send_mail(subject, message, email_from, recipient_list)
            user.save()
            return redirect('/code/verify/?email='+str(email))
        except Exception as e:
            messages.success(request, f"Failed to send verification email. Please try again.{e}")
            return redirect('regiter')
            
       
        # messages.success(request, "Registration successful!")
        # return redirect('user_login')
    
    return render(request, 'e_commerc/register.html')

'''
=====================================================================================================================================
                                                       register_verify method 
=====================================================================================================================================
'''


def register_verify(request):
    email = request.GET['email']
    try:
        user = Ecommerc_User.objects.get(email=email)
        if request.method == 'POST':     
            code = request.POST.get('code')
            if user.verify_code == code:
                u = Ecommerc_User.objects.get(email=user.email)
                u.status= True
                u.save()
                # request.session['user_uid'] = user.user_uid
                return redirect(f"/login/?next={request.get_full_path()}")
            else:
                messages.error(request, 'The verification code in incorrect.')  # 👈 Error Message
                return render(request, 'e_commerc/register_verify.html')
        
    except :
        messages.error(request, 'Email not register')  # 👈 Error Message
        return render(request, 'e_commerc/register_verify.html')
    
 
    messages.error(request, f'The verification code in {email}.')  # 👈 Error Message
    return render(request, 'e_commerc/register_verify.html')


'''
=====================================================================================================================================
                                                       forgot_password method 
=====================================================================================================================================
'''
# views.py


def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = Ecommerc_User.objects.get(email=email)
            otp = str(random.randint(100000, 999999))
            user.verify_code = otp
            # user.save()

            # Show OTP on terminal (you can integrate email sending here)
            request.session['reset_email'] = email
            subject = 'Hello send verify code!'
            message = f'Verification code is .{otp}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]  # Add recipient email addresses here
            try:
                send_mail(subject, message, email_from, recipient_list)
                user.save()
                return redirect('verify_otp')
            except Exception as e:
                messages.success(request, f"Failed to send verification email. Please try again.{e}")

        except Ecommerc_User.DoesNotExist:
            messages.error(request, "Email not registered.")
    return render(request, 'e_commerc/forgot_password.html')

'''
=====================================================================================================================================
                                                       verify_otp method 
=====================================================================================================================================
'''

def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get('otp')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        email = request.session.get('reset_email')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('verify_otp')
        try:
            user = Ecommerc_User.objects.get(email=email)
            if user.verify_code == entered_otp:
                user.password = password
                user.verify_code = ""
                user.save()
                messages.error(request, "Password reset successfully.")
                return redirect('login_user')
            else:
                messages.error(request, "Incorrect OTP.")
        except Ecommerc_User.DoesNotExist:
            messages.error(request, "Something went wrong.")
    return render(request, 'e_commerc/verify_otp.html')

'''
=====================================================================================================================================
                                                       load_navbar_data method 
=====================================================================================================================================
'''


from django.http import JsonResponse
def load_navbar_data(request):
    category = Category.objects.all()
    categories_data = [{'id': c.id, 'name': c.name,} for c in category]
    if 'user_uid' not in request.session:
      #  return redirect(f"/login/?next={request.get_full_path()}")
        categories = category 
        cart_count = 0 #request.session.get('cart_count', 0)  # Or calculate from cart model
        response_data = {
            'categories': categories_data,
            'cart_count': cart_count,
            'is_authenticated': False,
            'username': 'ranjeet'
        }
        return JsonResponse(response_data)
    else:
        user_uid = request.session.get('user_uid')
        user = Ecommerc_User.objects.get(user_uid = user_uid)
        cart_count = Cart.objects.filter(user_uid = user.user_uid).count()
        response_data = {
            'categories': categories_data,
            'cart_count': cart_count,
            'is_authenticated': True,
            'username': user.name
        }
        return JsonResponse(response_data)

'''
=====================================================================================================================================
                                                       ecoomerc_home method 
=====================================================================================================================================
'''


def ecoomerc_home(request):
    # if 'user_uid' not in request.session:
    #     return redirect(f"/login/?next={request.get_full_path()}")
    return redirect('all_products')
  #  return HttpResponse("ecoomerc_home")
  #  return render(request ,'e_commerc/login.html')

'''
=====================================================================================================================================
                                                       all_products method 
=====================================================================================================================================
'''
def all_products(request):
    
    products = Products.objects.all()
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    services =  MainService.objects.prefetch_related('sub_services').all()
    # return HttpResponse(name)
    return render(request, 'e_commerc/products.html', {'products': products , 'categories': categories,'subcategories':subcategories,
                                                       'services':services })

'''
=====================================================================================================================================
                                                       category_filter method 
=====================================================================================================================================
'''

# views.py
def category_filter(request, name):
    category = Category.objects.filter(name=name).first()
    products = Products.objects.filter(category=category)
    subcategory = SubCategory.objects.filter(category=category)
    services =  MainService.objects.prefetch_related('sub_services').all()
    # return HttpResponse(name)
    return render(request, 'e_commerc/products_by_category.html', {'products': products ,'categories': subcategory,
                                                                   'services':services})
'''
=====================================================================================================================================
                                                       sub_category_filter method 
=====================================================================================================================================
'''

# views.py
def sub_category_filter(request, name):
    subcategory = SubCategory.objects.filter(name=name).first()
    products = Products.objects.filter(subcategory=subcategory)
    subcategorys = SubCategory.objects.filter(category= subcategory.category)
    services =  MainService.objects.prefetch_related('sub_services').all()
    # return HttpResponse(name)
    return render(request, 'e_commerc/products_by_category.html', {'products': products ,'categories': subcategorys,
                                                                   'services':services})

'''
=====================================================================================================================================
                                                       product_detail method 
=====================================================================================================================================
'''

def product_detail(request, Product_id):
    products_dt = Products.objects.get(Product_id=Product_id)
    products = Products.objects.filter(model_name=products_dt.model_name)
    
    return render(request, 'e_commerc/product_dt.html', {'products': products ,'products_dt':products_dt})                                                                   

from django.http import JsonResponse
from django.shortcuts import redirect
from .models import Products, Ecommerc_User, Cart

# def add_to_cart(request):
#     if 'user_uid' not in request.session:
#         return JsonResponse({'success': False, 'message': 'Please log in to continue.', 'redirect_url': f"/login/?next={request.get_full_path()}"})

#     user_uid = request.session.get('user_uid')
#     try:
#         user = Ecommerc_User.objects.get(user_uid=user_uid)
#     except Ecommerc_User.DoesNotExist:
#         return JsonResponse({'success': False, 'message': 'User not found'})

#     if request.method == "POST":
#         product_id = request.POST.get('product_id')
#         quantity = int(request.POST.get('quantity', 1))
#         action = request.POST.get('action')

#         try:
#             product = Products.objects.get(Product_id=product_id)
#             Cart.objects.create(
#                     Product_id=str(product.Product_id),
#                     user_uid=user.user_uid,
#                     sku_code=product.sku_code,
#                     title=product.title,
#                     color=product.color,
#                     img1=product.image1,
#                     size="M",
#                     price=product.price,
#                     mrp=product.mrp,
#                     delivery_charges="0",
#                     discount="0%",
#                     total_amount=product.price * quantity,
#                     total_qty=str(quantity),
#                 )

#             if action == 'add_to_cart':
            
#                 return JsonResponse({'success': True, 'message': 'Product added to cart successfully.'})

#             elif action == 'buy_now':
#                 # Redirect to the checkout page with product details
#                 return JsonResponse({'success': True, 'message': 'Redirecting to checkout.', 'redirect_url': '/Cart-dt/'})

#         except Products.DoesNotExist:
#             return JsonResponse({'success': False, 'message': 'Product not found'})

#     return JsonResponse({'success': False, 'message': 'Invalid request'})

def add_to_cart(request):
    if 'user_uid' not in request.session:
        return JsonResponse({'success': False, 'message': 'Please log in to continue.', 'redirect_url': f"/login/?next={request.get_full_path()}"})

    user_uid = request.session.get('user_uid')
    try:
        user = Ecommerc_User.objects.get(user_uid=user_uid)
    except Ecommerc_User.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'User not found'})

    if request.method == "POST":
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        action = request.POST.get('action')

        try:
            product = Products.objects.get(Product_id=product_id)

            # ✅ Check if product is out of stock
            if product.quantity <= 0:
                return JsonResponse({'success': False, 'message': 'Product is out of stock'})

            # ✅ Check if requested quantity > available stock
            if quantity > product.quantity:
                return JsonResponse({'success': False, 'message': f'Only {product.quantity} items available in stock'})

            # ✅ Create cart item
            Cart.objects.create(
                Product_id=str(product.Product_id),
                user_uid=user.user_uid,
                sku_code=product.sku_code,
                title=product.title,
                color=product.color,
                img1=product.image1,
                size="M",
                price=product.price,
                mrp=product.mrp,
                delivery_charges="0",
                discount="0%",
                total_amount=product.price * quantity,
                total_qty=str(quantity),
            )

            if action == 'add_to_cart':
                return JsonResponse({'success': True, 'message': 'Product added to cart successfully.'})
            elif action == 'buy_now':
                return JsonResponse({'success': True, 'message': 'Redirecting to checkout.', 'redirect_url': '/Cart-dt/'})

        except Products.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Product not found'})

    return JsonResponse({'success': False, 'message': 'Invalid request'})



def checkout(request):
    return HttpResponse('checkout')

def Cart_dt(request):
    if 'user_uid' not in request.session:
            return redirect(f"/login/?next={request.get_full_path()}")
    user_uid = request.session.get('user_uid')
    
    user = Ecommerc_User.objects.get(user_uid=user_uid)
    categories = Category.objects.all()
    services =  MainService.objects.prefetch_related('sub_services').all()
    cart_product = Cart.objects.filter(user_uid = user.user_uid)

    cart_total = 0 
    for t in cart_product:
        cart_total = cart_total + float(t.total_amount)
    # return HttpResponse(name)
    request.session['cart_total'] = cart_total
    return render(request, 'e_commerc/Cart.html', {'categories': categories,'cart_product':cart_product,
                                                       'services':services ,'cart_total':cart_total})                         


from django.http import JsonResponse
from .models import Cart
from django.http import JsonResponse
from .models import Cart
import json

def update_cart(request):
    if 'user_uid' not in request.session:
        return redirect(f"/login/?next={request.get_full_path()}")
    
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            item_id = data.get('itemId')
            quantity = int(data.get('quantity'))

            # Check if item exists
            cart_item = Cart.objects.get(id=item_id)
            cart_item.total_qty = quantity
            cart_item.total_amount = int(cart_item.price) * quantity
            cart_item.save()

            return JsonResponse({"success": True})
        except Cart.DoesNotExist:
            return JsonResponse({"success": False, "error": "Item not found"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

def remove_cart(request):
    if 'user_uid' not in request.session:
        return redirect(f"/login/?next={request.get_full_path()}")
    
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            item_id = data.get('itemId')

            # Check if item exists and delete
            cart_item = Cart.objects.get(id=item_id)
            cart_item.delete()

            return JsonResponse({"success": True})
        except Cart.DoesNotExist:
            return JsonResponse({"success": False, "error": "Item not found"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
                   


######################################  CHECK OUT  METHOD CLOSE ###############################################


import razorpay
# Initialize Razorpay client
razorpay_key_id = 'rzp_live_6gbtU9z7ygopTT' 
razorpay_key_secret = '2ZO8skB29Sy7yHatvUKAoz6k'
webhook = ''
client_razorpay = razorpay.Client(auth=(razorpay_key_id, razorpay_key_secret))

@csrf_exempt
def Check_out(request):
    print('check_out')
    if 'user_uid' not in request.session:
        return redirect(f"/login/?next={request.get_full_path()}")
    
    user_uid = request.session.get('user_uid')
    user = Ecommerc_User.objects.get(user_uid=user_uid)
    categories = Category.objects.all()
    services =  MainService.objects.prefetch_related('sub_services').all()
    cart_total = request.session.get('cart_total')
    cart_items = Cart.objects.filter(user_uid = user.user_uid)
    try:
        print('run try')
        user_id = request.session.get('user_uid')
        cart_products = Cart.objects.filter(user_uid=user_id)
        cart_count = cart_products.count()
      
        user = Ecommerc_User.objects.get(user_uid=user_id)

        if request.method == 'POST':
            print('run post')
            # Extract form data
            firstName = request.POST.get('firstName')
            lastName = request.POST.get('lastName')
            mobileNumber = request.POST.get('mobileNumber')
            email = request.POST.get('email')
            houseNo = request.POST.get('houseNo')
            street = request.POST.get('street')
            street1 = request.POST.get('street1')
            street2 = request.POST.get('street2')
            pinCode = request.POST.get('pinCode')
            city = request.POST.get('city')
            country = request.POST.get('country')
            region = request.POST.get('region')

            payment_method = request.POST.get('payment_method')
                
            # Generate a unique order ID
            unique_id = uuid.uuid4()
            orderID =  str(unique_id.int)[:10]  
            order_id = str(orderID)+f'_{cart_count}_PD'
            order_date = datetime.now()

            # Ensure total_amount is numeric
            total_amount = 0
            for item in cart_products:
                # Convert total_amount to float if it's a string
                item_total = float(item.total_amount) if isinstance(item.total_amount, str) else item.total_amount
                total_amount += item_total

            cart_product = Cart.objects.filter(user_uid = user.user_uid)
            cart_total = 0 
            for t in cart_product:
                cart_total = cart_total + float(t.total_amount)

            total_amount *= 100  # in paise
            # Create Razorpay order
            razorpay_order = client_razorpay.order.create({
                'amount': total_amount,
                'currency': 'INR',
                'payment_capture': '1',
                'notes': {
                    'name': f'{firstName} {lastName}',
                    'phone': mobileNumber,
                }
            })
            payment_id = razorpay_order['id']
            if payment_method == 'cod':
                ord_status = 'New Orders'
                order_type = 'COD'
            else:
                ord_status = 'Failed Orders'
                order_type = 'Prepaid'
            # Save orders to your database
            for o in cart_products:
                order = Order(
                    email=email,
                    user_uid=user_id,
                    sku_code=o.sku_code,
                    Product_id=o.Product_id,
                    title=o.title,
                    price=o.price,
                    qty=o.total_qty,
                    total_amount=o.total_amount,
                    first_name=firstName,
                    last_name=lastName,
                    mobile_number=mobileNumber,
                    house_no=houseNo,
                    street=street,
                    street1=street1,
                    street2=street2,
                    pin_code=pinCode,
                    city=city,
                    country=country,
                    region=region,
                    order_id=order_id,
                    order_date=order_date,
                    order_status=ord_status,
                    order_type = order_type,
                    tracking_id="",
                    tracking_link="",
                    img1=o.img1,
                 
                )
                order.save()
                pd = Products.objects.get(Product_id = o.Product_id)
                qt = pd.quantity 
                pd.quantity = int(qt) - int(o.total_qty)
                pd.save()
            # Clear cart
            # remove_all(request)
            if payment_method == 'cod':
                remove_all(request)
                return render(request, 'e_commerc/orderconform.html', {'pese': cart_total, 'orderid': order_id, 'payment_id': 'COD'})
            
            return render(request, 'e_commerc/payment.html', {
                'pese': total_amount // 100,
                'orderid': order_id,
                'payment_id': payment_id,
                'razorpay_key_id':razorpay_key_id,
                'first_name': f'{firstName} {lastName}'

            })

        data = {
            'categories': categories,'cart_items':cart_items,
                                                       'services':services ,'cart_total':cart_total
        }

        return render(request, 'e_commerc/Check_out.html', data)                         


    except Exception as e:
        return redirect(f"/login/?next={request.get_full_path()}")



import json
@csrf_exempt
def razorpay_webhook(request):
    if request.method == "POST":
        try:
            # Parse the webhook payload
            payload = request.body.decode('utf-8')
            event = json.loads(payload)

            # Verify the webhook signature
            signature = request.headers.get('X-Razorpay-Signature')
            if not client_razorpay.utility.verify_webhook_signature(payload, signature, webhook ):
                return JsonResponse({'error': 'Invalid signature'}, status=400)

            # Handle the event
            if event['event'] == 'payment.captured':
                payment_id = event['payload']['payment']['entity']['id']
                order_id = event['payload']['payment']['entity']['order_id']
                # Update the payment status in your database here

            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid method'}, status=405)
 
######################################  PAYMENT  METHOD START ##################################################

def pay_status(request):
    # try:
        if request.method == 'GET':
            client = razorpay.Client(auth=(razorpay_key_id, razorpay_key_secret))
            payment_id = request.GET.get('payment_id')
            orderid = request.GET.get('orderid')
            pese = request.GET.get('pese')

            payment = client.payment.fetch(payment_id)
            remove_all(request)
            if payment['status'] == 'captured':
                print('razorpay_key_id = ',razorpay_key_id)
                ttt = Order.objects.get(order_id=orderid)
                ttt.order_status = "New"
                ttt.payment_id = payment_id
                ttt.save()
                remove_all(request)
                return render(request, 'e_commerc/orderconform.html', {'pese': pese, 'orderid': orderid, 'payment_id': payment_id})
            else:
                return HttpResponse("Payment failed!")

        return HttpResponse("Method Not Allowed")


def remove_all(request):
    try:
        user_id = request.session.get('user_uid')
        if not user_id:
            return redirect('/login/?message=Please login')

        cart_products = Cart.objects.filter(user_uid=user_id)
        cart_products.delete()
    except:
        return redirect('/login/?message=Please login')

def get_order_counts(user_id):
    return {
        'all_orders_count': Order.objects.filter(user_uid=user_id).count(),
        'shipped_orders_count': Order.objects.filter(user_uid=user_id, order_status='Shipped Orders').count(),
        'new_orders_count': Order.objects.filter(user_uid=user_id, order_status='New Orders').count(),
        'delivered_orders_count': Order.objects.filter(user_uid=user_id, order_status='Delivered Orders').count(),
        'ready_orders_count': Order.objects.filter(user_uid=user_id, order_status='Ready Orders').count(),
        'cancelled_orders_count': Order.objects.filter(user_uid=user_id, order_status='Cancelled Orders').count(),
        'failed_orders_count': Order.objects.filter(user_uid=user_id, order_status='Failed Orders').count(),
    }



'''
=====================================================================================================================================
                                                       profile method 
=====================================================================================================================================
'''
from service.models import *
def profile(request):
    print('profile')
    if 'user_uid' not in request.session:
        print('login')
        print(f'request.get_full_path() = {request.get_full_path()}')
        return redirect(f"/login/?next={request.get_full_path()}")
    user_id = request.session.get('user_uid')
    
    user = Ecommerc_User.objects.get(user_uid=user_id)
    order_counts = get_order_counts(user_id)
    all_orders = Order.objects.filter(user_uid=user_id).order_by('-id')


    return render(request, 'e_commerc/profile.html',{"user":user,
                                                      **order_counts,
                                                       'orders': all_orders,
                                                            })

# Main All Orders View
def user_all_order(request):
    if 'user_uid' not in request.session:
        return redirect(f"/login/?next={request.get_full_path()}")

    user_id = request.session.get('user_uid')
    all_orders = Order.objects.filter(user_uid=user_id).order_by('-id')
    order_counts = get_order_counts(user_id)

    data = {
        'orders': all_orders,
        'selected_status': 'All',
        **order_counts,
    }
    return render(request, 'e_commerc/orders.html', data)

from urllib.parse import unquote  
# Filtered Status View
def user_all_order_by_status(request, status):
    if 'user_uid' not in request.session:
        return redirect(f"/login/?next={request.get_full_path()}")

    user_id = request.session.get('user_uid')

    status = unquote(status)
    print(f'Decoded status = {status}')

    # Validate status
    valid_statuses = [choice[0] for choice in Order.ORDER_STATUS_CHOICES]
    if status not in valid_statuses:
        return redirect('user_all_order')

    filtered_orders = Order.objects.filter(user_uid=user_id, order_status=status).order_by('-id')
    order_counts = get_order_counts(user_id)

    data = {
        'orders': filtered_orders,
        'selected_status': status,
        **order_counts,
    }
    return render(request, 'e_commerc/orders.html', data)
