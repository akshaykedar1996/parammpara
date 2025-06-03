from django.db import models

# Create your models here.
from django.db import models

class CarouselImage(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='carousel_images/')  # Media folder me save hoga
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


from django.db import models

# Main Service Model
class MainService(models.Model):
    title = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='services/', blank=True, null=True)

    def __str__(self):
        return self.title

# Sub Service Model
class SubService(models.Model):
    main_service = models.ForeignKey(MainService, on_delete=models.CASCADE, related_name='sub_services')
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='sub_services/', blank=True, null=True)
    description = models.TextField()
    faqs = models.TextField(help_text="Enter FAQs separated by '|'")  # Multiple FAQs ko store karne ke liye
    
    def get_faqs(self):
        return self.faqs.split('|')  # FAQs ko list me convert karega

    def __str__(self):
        return f"{self.main_service.title} - {self.title}"
    


class Testimonials(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    description1 = models.TextField()
    post = models.TextField(blank=True, null=True)
    

    def __str__(self):
        return f"{self.title}"    

from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    contact_no = models.CharField(max_length=15)
  
    
    msg = models.TextField()
    status = models.BooleanField(default=False,blank=True,null=True)

    def __str__(self):
        return f"{self.name} "



from django.db import models

class Franchise(models.Model):
    name = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=15)
    email = models.EmailField()
    date = models.DateField()
    time = models.TimeField()
    address = models.TextField()
    status = models.BooleanField(default=False,blank=True,null=True)
    
    def __str__(self):
        return f"{self.name} - {self.date} {self.time}"
    
    
    
# =========franchise service model=========================
class Franchiseservice(models.Model):
    img1 = models.ImageField(upload_to='photos/', blank=True, null=True, max_length=200)
    title = models.CharField(max_length=500, blank=True, null=True)
    paragraph = models.CharField(max_length=500, blank=True, null=True)
    description = models.CharField(max_length=1500, blank=True, null=True)
    img2 = models.ImageField(upload_to='photos/', blank=True, null=True, max_length=200)

    def __str__(self):
        return self.title or "Service"
