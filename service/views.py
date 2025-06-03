from django.shortcuts import render , HttpResponse ,redirect,HttpResponseRedirect
from .models import *
from django.core.mail import send_mail
from django.conf import settings
from ecommerce.models import *
# Create your views here.
def home(request):
    images = CarouselImage.objects.all()  # Database se saari images fetch karenge
    services =  MainService.objects.prefetch_related('sub_services').all()
   
    ts = Testimonials.objects.all()
    products = Products.objects.all()
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        contact_msg = Contact.objects.create(
                name=name,
                email=email,
                contact_no=phone,
                msg=message
            )
        contact_msg.save()
        subject=f"New Contact Message from {name}",
        message=f"Name: {name}\nEmail: {email}\nSubject: {subject}\n\nMessage:\n{message}",
        fail_silently=False,       
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]  # Add recipient email addresses here
        try:
            send_mail(subject, message, email_from, recipient_list, fail_silently)
        except:
            pass    
            
        messages.success(request, "Your message has been sent successfully!")
        return HttpResponseRedirect('/#contact')

    return render(request, "index.html", {"images": images , 'services':services ,'testimonial':ts , 'products':products})


def service(request):
    services = MainService.objects.prefetch_related('sub_services').all()
    sub_service = SubService.objects.all()
    dt = {'services':services , 
          'sub_service':sub_service
          }
    return render(request, "services.html",dt)

def service_detail_view(request, service_id):
    service = MainService.objects.get(id=service_id)
    return redirect('service')
  

from django.shortcuts import render, get_object_or_404
from .models import SubService

def sub_service_detail(request, id):
    sub_service= SubService.objects.get(id=id)
    sub_service_all = SubService.objects.all()
    services = MainService.objects.prefetch_related('sub_services').all()

    dt = {'services':services , 
          'sub_service':sub_service_all,
          'sub': sub_service
          }
   
    # return HttpResponse(sub_service)
    return render(request, 'sub_service_detail.html', dt)



def abouts(request):
   
    sub_service_all = SubService.objects.all()
    services = MainService.objects.prefetch_related('sub_services').all()

    dt = {'services':services , 
          'sub_service':sub_service_all,
          
          }
   
    # return HttpResponse(sub_service)
    return render(request, 'abouts.html', dt)




from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import FranchiseForm
from .models import Franchise


def Contact_us(request):
    sub_service_all = SubService.objects.all()
    services = MainService.objects.prefetch_related('sub_services').all()

    if request.method == "POST":
        post_data = request.POST.copy()
        country_code = post_data.get('country_code')
        contact_number = post_data.get('contact_no')
        full_contact = f"{country_code}{contact_number}"
        post_data['contact_no'] = full_contact

        form = FranchiseForm(post_data)

        if form.is_valid():
            franchise = form.save()

            # Send confirmation email
            subject = "Franchise Confirmation"
            message = f"""
            Dear {franchise.name},

            Thank you for booking a contact with us. Here are your details:
            📅 Date: {franchise.date}
            🕒 Time: {franchise.time}
            📍 Address: {franchise.address}

            We look forward to seeing you!

            Best regards,
            Your Company Name
            """
            recipient_email = franchise.email
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient_email])
            except Exception as e:
                print("Email failed:", e)

            messages.success(request, "Your appointment has been booked successfully! 🎉")
            return redirect('Contact_us')  # Change to your actual URL name
        else:
            messages.error(request, "There was an error in your form. Please check the details. ❌")
    else:
        form = FranchiseForm()

    return render(request, 'ContactUs.html', {
        'services': services,
        'sub_service': sub_service_all,
        'form': form
    })




def franchise(request):
   
    sub_service_all = SubService.objects.all()
    franchise_service_all = Franchiseservice.objects.all()
    services = MainService.objects.prefetch_related('sub_services').all()

    dt = {'services':services , 
          'sub_service':sub_service_all,
          'franchise_service_all':franchise_service_all,
          
          }
   
    # return HttpResponse(sub_service)
    return render(request, 'franchise.html', dt)


################################# ADD SERVICES ###################################
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Franchiseservice
from .forms import ServiceForm

# Add new service
@csrf_exempt
def add_services(request):
    if not request.session.get('user_id'):
        return redirect('/subadmin/?message=Please login')

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/subadmin/dashboard/')
    else:
        form = ServiceForm()

    return render(request, 'Subadmin_Addcards.html', {'ServiceForm': form})


# View all services for subadmin
def services_list(request):
    if not request.session.get('user_id'):
        return redirect('/subadmin/?message=Please login')

    all_service = Franchiseservice.objects.all()
    return render(request, 'Subadmin_Allservice.html', {'all_service': all_service})


# Edit existing service
def edit_services(request):
    if not request.session.get('user_id'):
        return redirect('/subadmin/?message=Please login')

    service_id = request.GET.get('idd')
    service_instance = get_object_or_404(Franchiseservice, id=service_id)

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service_instance)
        if form.is_valid():
            form.save()
            return redirect('/subadmin/dashboard/') 
    else:
        form = ServiceForm(instance=service_instance)

    return render(request, 'Subadmin_editservice.html', {'form': form, 'service': service_instance})


# Public view of services
def services_page(request):
    services = Franchiseservice.objects.all()
    return render(request, 'services.html', {'services': services})


# Read more view
def read_more_view(request, service_id):
    service_obj = get_object_or_404(Franchiseservice, id=service_id)
    return render(request, 'read_more.html', {'service': service_obj})
