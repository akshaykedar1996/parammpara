from django.shortcuts import render,HttpResponse

from django.shortcuts import render, redirect, get_object_or_404
from service.models import *
from .forms import CarouselImageForm
from .models import AdminDT
from ecommerce.models import *
# Create your views here.
def login_admin(request):
    if request.method == 'POST':
    
        email = request.POST.get('Email')
        password = request.POST.get('password')
        try:
            admindt = AdminDT.objects.get(admin_email = email)
            if password == admindt.admin_password:

                request.session['admin_id'] = admindt.admin_id
                return redirect('super_index')
            else:
                messages.error(request, 'Wrong password.') 
        except:
            messages.error(request, 'Admin not found.') 
    return render(request , 'superadmin/login.html')


def logout_admin(request):
    if 'admin_id' in request.session:
        del request.session['admin_id']
    return redirect('login_admin')



# Create your views here.
def home(request):
    if 'admin_id' not in request.session:
        return redirect('login_admin')
    contacts = Contact.objects.all().count()
    franchise = Franchise.objects.all().count()

    contacts_p = Contact.objects.filter(status = True).count()
    appointment_p = Franchise.objects.filter(status = True).count()

    contacts_f = Contact.objects.filter(status = False).count()
    appointment_f = Franchise.objects.filter(status = False).count()
    order_counts = get_order_counts()
    from datetime import date


    from django.db.models import Sum
    from datetime import date

    # Filter today's orders
    today_orders = Order.objects.filter(order_date__date=date.today()).order_by('-id')
    today_sale = today_orders.aggregate(total=Sum('total_amount'))['total'] or 0

    # All orders
    all_orders = Order.objects.all()
    all_sale = all_orders.aggregate(total=Sum('total_amount'))['total'] or 0

    pd = Products.objects.all()
    out_of_stock_count = pd.filter(quantity=0).count()
    in_stock_count = pd.filter(quantity__gt=0).count()
    active_product_count = pd.filter(is_available=True).count()

    

    dt={
        'contacts':contacts,
        'appointment':franchise,
        'contacts_p':contacts_p,
        'appointment_p':appointment_p,

        'contacts_f':contacts_f,
        'appointment_f':appointment_f,
        **order_counts,
        'today_orders_count':today_orders.count(),
        'today_orders':today_orders,
        'today_sale':today_sale,
        'all_sale':all_sale,

        'all_pd':pd.count(),
        'out_of_stock_count': out_of_stock_count,
        'in_stock_count': in_stock_count,
        'active_product_count': active_product_count,
       

    }
    return render(request, 'superadmin/dashboard.html',dt)

'''
======================================================  carousel ===================================================== 
'''
# views.py carousel_list



def carousel_list(request):
    if 'admin_id' not in request.session:
        return redirect('login_admin')
    images = CarouselImage.objects.all()
    return render(request, 'superadmin/carousel/list.html', {'images': images})

def carousel_add(request):
    if 'admin_id' not in request.session:
        return redirect('login_admin')
    if request.method == 'POST':
        form = CarouselImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('carousel_list')
    else:
        form = CarouselImageForm()
    return render(request, 'superadmin/carousel/form.html', {'form': form, 'title': 'Add Carousel Image'})

def carousel_edit(request, pk):
    if 'admin_id' not in request.session:
        return redirect('login_admin')
    image = get_object_or_404(CarouselImage, pk=pk)
    if request.method == 'POST':
        form = CarouselImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            form.save()
            return redirect('carousel_list')
    else:
        form = CarouselImageForm(instance=image)
    return render(request, 'superadmin/carousel/form.html', {'form': form, 'title': 'Edit Carousel Image'})

def carousel_delete(request, pk):
    if 'admin_id' not in request.session:
        return redirect('login_admin')
    image = get_object_or_404(CarouselImage, pk=pk)
    if request.method == 'POST':
        image.delete()
        return redirect('carousel_list')
    return render(request, 'superadmin/carousel/confirm_delete.html', {'image': image})


'''
======================================================  mainservice_list ===================================================== 
'''
from django.shortcuts import render, redirect, get_object_or_404
from .forms import MainServiceForm, SubServiceForm

# ------- Main Service Views -------
def mainservice_list(request):
    if 'admin_id' not in request.session:
        return redirect('login_admin')
    services = MainService.objects.all()
    return render(request, 'superadmin/services/mainservice_list.html', {'services': services})

def mainservice_add(request):
    if 'admin_id' not in request.session:
        return redirect('login_admin')
    form = MainServiceForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('mainservice_list')
    return render(request, 'superadmin/services/mainservice_form.html', {'form': form, 'title': 'Add Main Service'})

def mainservice_edit(request, pk):
    if 'admin_id' not in request.session:
        return redirect('login_admin')
    service = get_object_or_404(MainService, pk=pk)
    form = MainServiceForm(request.POST or None, request.FILES or None, instance=service)
    if form.is_valid():
        form.save()
        return redirect('mainservice_list')
    return render(request, 'superadmin/services/mainservice_form.html', {'form': form, 'title': 'Edit Main Service'})

def mainservice_delete(request, pk):
    if 'admin_id' not in request.session:
        return redirect('login_admin')
    service = get_object_or_404(MainService, pk=pk)
    if request.method == 'POST':
        service.delete()
        return redirect('mainservice_list')
    return render(request, 'superadmin/services/mainservice_confirm_delete.html', {'service': service})


# ------- Sub Service Views -------
def subservice_list(request):
    if 'admin_id' not in request.session:
        return redirect('login_admin')
    services = SubService.objects.all()
    return render(request, 'superadmin/services/subservice_list.html', {'services': services})

def subservice_add(request):
    if 'admin_id' not in request.session:
        return redirect('login_admin')
    form = SubServiceForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('subservice_list')
    return render(request, 'superadmin/services/subservice_form.html', {'form': form, 'title': 'Add Sub Service'})

def subservice_edit(request, pk):
    if 'admin_id' not in request.session:
        return redirect('login_admin')
    service = get_object_or_404(SubService, pk=pk)
    form = SubServiceForm(request.POST or None, request.FILES or None, instance=service)
    if form.is_valid():
        form.save()
        return redirect('subservice_list')
    return render(request, 'superadmin/services/subservice_form.html', {'form': form, 'title': 'Edit Sub Service'})

def subservice_delete(request, pk):
    if 'admin_id' not in request.session:
        return redirect('login_admin')
    service = get_object_or_404(SubService, pk=pk)
    if request.method == 'POST':
        service.delete()
        return redirect('subservice_list')
    return render(request, 'superadmin/services/subservice_confirm_delete.html', {'service': service})



'''
======================================== testimonials_list ===================================
'''

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TestimonialsForm
from django.contrib import messages

def testimonials_list(request):
    if 'admin_id' not in request.session:
        return redirect('login_admin')
    testimonials = Testimonials.objects.all()
    return render(request, 'superadmin/testimonials/testimonials_list.html', {'testimonials': testimonials})

def add_testimonial(request):
    if 'admin_id' not in request.session:
        return redirect('login_admin')
    if request.method == 'POST':
        form = TestimonialsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Testimonial added successfully.')
            return redirect('testimonials_list')
    else:
        form = TestimonialsForm()
    return render(request, 'superadmin/testimonials/testimonials_form.html', {'form': form, 'title': 'Add Testimonial'})

def edit_testimonial(request, pk):
    if 'admin_id' not in request.session:
        return redirect('login_admin')
    testimonial = get_object_or_404(Testimonials, pk=pk)
    if request.method == 'POST':
        form = TestimonialsForm(request.POST, request.FILES, instance=testimonial)
        if form.is_valid():
            form.save()
            messages.success(request, 'Testimonial updated successfully.')
            return redirect('superadmin/testimonials_list')
    else:
        form = TestimonialsForm(instance=testimonial)
    return render(request, 'superadmin/testimonials/testimonials_form.html', {'form': form, 'title': 'Edit Testimonial', 'testimonial': testimonial})

def delete_testimonial(request, pk):
    if 'admin_id' not in request.session:
        return redirect('login_admin')
    testimonial = get_object_or_404(Testimonials, pk=pk)
    if request.method == 'POST':
        testimonial.delete()
        messages.success(request, 'Testimonial deleted successfully.')
        return redirect('testimonials_list')
    return render(request, 'superadmin/testimonials/testimonials_confirm_delete.html', {'testimonial': testimonial})

""" 
======================================================================================================================
"""

from django.shortcuts import render, redirect, get_object_or_404

# Appointment List
def Franchise_list(request):
    if 'admin_id' not in request.session:
        return redirect('login_admin')
    franchise = Franchise.objects.all()
    return render(request, 'superadmin/Franchise_list.html', {'franchise': franchise, 'title': 'Franchise Client List'})

# Appointment Status Toggle
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


def toggle_appointment_status(request, pk):
    if 'admin_id' not in request.session:
        return redirect('login_admin')
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        franchise = get_object_or_404(Franchise, pk=pk)
        franchise.status = not franchise.status
        franchise.save()
        return JsonResponse({
            'success': True,
            'new_status': franchise.status,
            'status_label': 'Active' if franchise.status else 'Inactive',
            'badge_class': 'bg-success' if franchise.status else 'bg-danger',
            'button_class': 'btn-danger' if franchise.status else 'btn-success',
            'button_text': 'Deactivate' if franchise.status else 'Activate'
        })
    return JsonResponse({'success': False}, status=400)



# Contact List
def contact_list(request):
    if 'admin_id' not in request.session:
        return redirect('login_admin')
    contacts = Contact.objects.all()
    return render(request, 'superadmin/contact_list.html', {'contacts': contacts, 'title': 'Contact List'})

from django.http import JsonResponse
from django.shortcuts import get_object_or_404


def toggle_contact_status(request, pk):
    if 'admin_id' not in request.session:
        return redirect('login_admin')
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        contact = get_object_or_404(Contact, pk=pk)
        contact.status = not contact.status
        contact.save()
        return JsonResponse({
            "success": True,
            "new_status": contact.status,
            "status_label": "Active" if contact.status else "Inactive",
            "badge_class": "bg-success" if contact.status else "bg-danger",
            "button_class": "btn-danger" if contact.status else "btn-success",
            "button_text": "Deactivate" if contact.status else "Activate"
        })
    return JsonResponse({"success": False}, status=400)


# views.py
from django.shortcuts import render, get_object_or_404, redirect

from ecommerce.models import *
from .forms import *

def product_list(request):
    if 'admin_id' not in request.session:
        return redirect('login_admin')
    products = Products.objects.all()
    return render(request, 'superadmin/products/product_list.html', {'products': products})

def product_create(request):
    if 'admin_id' not in request.session:
        return redirect('login_admin')
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'superadmin/products/product_form.html', {'form': form})

def product_update(request, pk):
    if 'admin_id' not in request.session:
        return redirect('login_admin')
    product = get_object_or_404(Products, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'superadmin/products/product_form.html', {'form': form})

def product_delete(request, pk):
    if 'admin_id' not in request.session:
        return redirect('login_admin')
    product = get_object_or_404(Products, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'superadmin/products/product_confirm_delete.html', {'product': product})








# views.py
from django.shortcuts import render, get_object_or_404, redirect


# Category Views
def category_list(request):
    if 'admin_id' not in request.session:
        return redirect('login_admin')
    categories = Category.objects.all()
    return render(request, 'superadmin/ProductCT/category_list.html', {'categories': categories})

def category_create(request):
    if 'admin_id' not in request.session:
        return redirect('login_admin')
    if request.method == 'POST':
        form = ProductCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = ProductCategoryForm()
        
    return render(request, 'superadmin/ProductCT/category_form.html', {'form': form})

def category_update(request, pk):
    if 'admin_id' not in request.session:
        return redirect('login_admin')
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = ProductCategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = ProductCategoryForm(instance=category)
    return render(request, 'superadmin/ProductCT/category_form.html', {'form': form})

def category_delete(request, pk):
    if 'admin_id' not in request.session:
        return redirect('login_admin')
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'superadmin/ProductCT/category_confirm_delete.html', {'category': category})

# SubCategory Views
def subcategory_list(request):
    if 'admin_id' not in request.session:
        return redirect('login_admin')
    subcategories = SubCategory.objects.all()
    return render(request, 'superadmin/ProductCT/subcategory_list.html', {'subcategories': subcategories})

def subcategory_create(request):
    if 'admin_id' not in request.session:
        return redirect('login_admin')
    if request.method == 'POST':
        form = ProductSubCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('subcategory_list')
    else:
        form = ProductSubCategoryForm()
    return render(request, 'superadmin/ProductCT/subcategory_form.html', {'form': form})

def subcategory_update(request, pk):
    if 'admin_id' not in request.session:
        return redirect('login_admin')
    subcategory = get_object_or_404(SubCategory, pk=pk)
    if request.method == 'POST':
        form = ProductSubCategoryForm(request.POST, request.FILES, instance=subcategory)
        if form.is_valid():
            form.save()
            return redirect('subcategory_list')
    else:
        form = ProductSubCategoryForm(instance=subcategory)
    return render(request, 'superadmin/ProductCT/subcategory_form.html', {'form': form})

def subcategory_delete(request, pk):
    if 'admin_id' not in request.session:
        return redirect('login_admin')
    subcategory = get_object_or_404(SubCategory, pk=pk)
    if request.method == 'POST':
        subcategory.delete()
        return redirect('subcategory_list')
    return render(request, 'superadmin/ProductCT/subcategory_confirm_delete.html', {'subcategory': subcategory})



'''
=====================================================================================================================================
                                                       product_detail method 
=====================================================================================================================================
'''

def product_detail(request, Product_id):
    if 'admin_id' not in request.session:
        return redirect('login_admin')
    print(f'Product_id = {Product_id}')
    products_dt = Products.objects.get(Product_id=Product_id)
    products = Products.objects.filter(model_name=products_dt.model_name)
    
    return render(request, 'superadmin/products/product_dt.html', {'products': products ,'products_dt':products_dt}) 

def get_order_counts():
    return {
        'all_orders_count': Order.objects.filter().count(),
        'shipped_orders_count': Order.objects.filter( order_status='Shipped Orders').count(),
        'new_orders_count': Order.objects.filter( order_status='New Orders').count(),
        'delivered_orders_count': Order.objects.filter( order_status='Delivered Orders').count(),
        'ready_orders_count': Order.objects.filter( order_status='Ready Orders').count(),
        'cancelled_orders_count': Order.objects.filter( order_status='Cancelled Orders').count(),
        'failed_orders_count': Order.objects.filter( order_status='Failed Orders').count(),
    }


def orders(request):
    if 'admin_id' not in request.session:
        return redirect('login_admin')

    admin_id = request.session.get('admin_id')
    admin = AdminDT.objects.get(admin_id=admin_id)
            
        # all_orders = Order.objects.all() 
        
    orders = Order.objects.all().order_by('-id')
   
    order_counts = get_order_counts()
    data={'orders':orders,
              **order_counts,
        }

    return render (request,'superadmin/Orders/Orders.html', data)

# views.py
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import redirect, get_object_or_404
def update_order_status(request):
    if 'admin_id' not in request.session:
        return redirect('login_admin')

    admin_id = request.session.get('admin_id')
    admin = AdminDT.objects.get(admin_id=admin_id)

    order_id = request.GET.get('id')
    action = request.GET.get('action')

    # Get all orders with this order_id
    orders = Order.objects.filter(order_id=order_id)

    if not orders.exists():
        return HttpResponse("Order not found", status=404)

    for order in orders:
        if action == 'accept':
            order.order_status = 'Ready Orders'

        elif action == 'ship':
            order.order_status = 'Shipped Orders'
            order.tracking_id = request.GET.get('tracking_id')
            order.tracking_link = request.GET.get('link')

        elif action == 'deliver':
            order.order_status = 'Delivered Orders'

        elif action == 'cancel':
            order.order_status = 'Cancelled Orders'

        order.save()

    return redirect('orders')

from urllib.parse import unquote
from datetime import date
# Filtered Status View
def admin_all_order_by_status(request, status):
    print(f'status = {status}')
    if 'admin_id' not in request.session:
        return redirect('login_admin')

    admin_id = request.session.get('admin_id')
    admin = AdminDT.objects.get(admin_id=admin_id)
    # Decode URL-encoded status (like 'New%20Orders' to 'New Orders')
    status = unquote(status)
    print(f'Decoded status = {status}')
    
    # Validate status
    valid_statuses = [choice[0] for choice in Order.ORDER_STATUS_CHOICES]
    print(f'valid_statuses = {valid_statuses}')
    if status not in valid_statuses:
        return redirect('orders')

    if status == 'Today Orders':
        filtered_orders = Order.objects.filter(order_date__date=date.today()).order_by('-id')
    else:    
        filtered_orders = Order.objects.filter( order_status=status).order_by('-id')
    order_counts = get_order_counts()

    data = {
        'orders': filtered_orders,
        'selected_status': status,
        **order_counts,
    }
    return render (request,'superadmin/Orders/Orders.html', data)


from django.shortcuts import render, get_list_or_404

def order_invoice(request, order_id):
    if 'admin_id' not in request.session:
        return redirect('login_admin')
    print(f'order_id = {order_id}')
    orders = Order.objects.filter(order_id=order_id)

    if not orders.exists():
        return render(request, 'superadmin/Orders/order_invoice.html', {'orders': []})
    
    # First order object to get common info like name, address, etc.
    order = orders.first()
    total_amount = sum(float(item.total_amount) for item in orders)
    return render(request, 'superadmin/Orders/order_invoice.html', {
        'orders': orders,
        'order': order,
        'grand_total': total_amount
    })