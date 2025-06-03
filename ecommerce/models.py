from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
import uuid

class Ecommerc_User(models.Model):
  #  user_uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user_uid = models.CharField(max_length=8, unique=True, default=uuid.uuid4().hex[:8])
    name = models.CharField(max_length=300,blank=True,null=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    Created_date = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=255)  # Added password field
    verify_code = models.CharField(blank=True, null=True, max_length=10,) 
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    status = models.BooleanField(default=False)


from django.db import models

# Main Category Model
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='Category/',blank=True, null=True)

    def __str__(self):
        return self.name


# SubCategory Model
class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='SubCategory/',blank=True, null=True)

    def __str__(self):
        return f"{self.category.name} → {self.name}"


# Product Model
class Products(models.Model):  
    Product_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    model_name = models.CharField(max_length=200, blank=True, null=True)
    sku_code = models.CharField(max_length=500, blank=True, null=True)
    brand = models.CharField(max_length=500, blank=True, null=True)

    name = models.CharField(max_length=500, blank=True, null=True)
    title = models.CharField(max_length=500, blank=True, null=True)
    sub_title = models.CharField(max_length=500, blank=True, null=True)

    price = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    mrp = models.IntegerField(blank=True, null=True)

    color = models.CharField(max_length=500, blank=True, null=True)
    quantity = models.PositiveIntegerField()
    description = models.TextField()

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True)

    updated_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)

    image1 = models.ImageField(upload_to='product_images/')
    image2 = models.ImageField(upload_to='product_images/')
    image3 = models.ImageField(upload_to='product_images/',blank=True, null=True)
    image4 = models.ImageField(upload_to='product_images/',blank=True, null=True)
    image5 = models.ImageField(upload_to='product_images/',blank=True, null=True)

    rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_bestselling = models.BooleanField(default=False)

    
    def __str__(self):
        return self.name



class Cart(models.Model):
    Product_id = models.CharField(max_length=500, null=True, blank=True)
    user_uid = models.CharField(max_length=550,null=True, blank=True)
    sku_code = models.CharField(max_length=550,null=True, blank=True)
    title= models.CharField(max_length=350,null=True, blank=True)
    color = models.CharField(max_length=550,null=True, blank=True)  # Rang
    img1 = models.ImageField(upload_to='photos/', blank=True, null=True,max_length=200, )
    size = models.CharField(max_length=330,null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    mrp = models.IntegerField(null=True, blank=True)
    delivery_charges = models.CharField(max_length=30,null=True, blank=True)
    discount = models.CharField(max_length=530,null=True, blank=True)
    total_amount = models.CharField(max_length=530,null=True, blank=True)
    total_qty = models.CharField(max_length=530,null=True, blank=True)


class Order(models.Model):
    Product_id = models.CharField(max_length=550, null=True, blank=True)
    user_uid = models.CharField(max_length=550,null=True, blank=True)

    first_name = models.CharField(max_length=500 ,null=True, blank=True)
    last_name = models.CharField(max_length=500 ,null=True, blank=True)
    mobile_number = models.CharField(max_length=20,null=True, blank=True)
    email = models.EmailField()

    house_no = models.CharField(max_length=50, blank=True, null=True)
    street = models.CharField(max_length=500, blank=True, null=True)
    street1 = models.CharField(max_length=500, blank=True, null=True)
    street2 = models.CharField(max_length=500, blank=True, null=True)
    pin_code = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=500, blank=True, null=True)
    country = models.CharField(max_length=500, default='India',blank=True, null=True)
    region = models.CharField(max_length=500, blank=True, null=True)

    payment_id = models.CharField(max_length=1000,null=True, blank=True)
    order_id =models.CharField(max_length=1000,null=True, blank=True)  # State name
    order_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    tracking_id=models.CharField(max_length=1000,null=True, blank=True)  # State name
    tracking_link=models.CharField(max_length=100,null=True, blank=True)  # State name
    ORDER_STATUS_CHOICES = [
         ('Pending Orders', 'Pending Orders'),
        ('New Orders', 'New Orders'),
        ('Ready Orders', 'Ready Orders'),
        ('Shipped Orders', 'Shipped Orders'),
        ('Delivered Orders', 'Delivered Orders'),
        ('Cancelled Orders', 'Cancelled Orders'),
        ('Failed Orders', 'Failed Orders'),
    ]
    
    order_status = models.CharField(
        max_length=50,
        choices=ORDER_STATUS_CHOICES,
        default='New Orders',
        null=True,
        blank=True
    )

    ORDER_TYPE_CHOICES = [
         ('COD', 'COD'),
        ('Prepaid', 'Prepaid'),
       
    ]
    
    order_type= models.CharField(
        max_length=50,
        choices=ORDER_TYPE_CHOICES,
        default='COD',
        null=True,
        blank=True
    )

    sku_code = models.CharField(max_length=500, blank=True, null=True)
    title = models.CharField(max_length=500, blank=True, null=True)

    total_amount = models.CharField(max_length=300,null=True, blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=2,null=True, blank=True)
    qty = models.CharField(max_length=300,null=True, blank=True)
    img1 = models.ImageField(upload_to='photos/', blank=True, null=True,max_length=200, )


    def __str__(self):
        return f'{self.first_name} {self.last_name}'
