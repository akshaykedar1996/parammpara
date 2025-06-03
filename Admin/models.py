from django.db import models
import uuid

# Create your models here.

# Create your models here.
class AdminDT(models.Model):
    admin_id = models.CharField(max_length=8, unique=True, blank=True, default=uuid.uuid4().hex[:8])
    admin_name = models.CharField(max_length=50, blank=True, null=True)
    admin_email = models.EmailField(blank=True, null=True)
    admin_password = models.CharField(max_length=50,blank=True, null=True)
    admin_phone_number = models.CharField(max_length=15,blank=True, null=True)
    admin_verify_code = models.CharField(max_length=15,blank=True, null=True)

    is_staff= models.BooleanField(default=False)    

    def save(self, *args, **kwargs):
        # Generate a new unique ID if admin_id is not set
        if not self.admin_id:
            self.admin_id = self.generate_unique_id()
        super(AdminDT, self).save(*args, **kwargs)
    
    def generate_unique_id(self):
        # Generate and return a unique ID
        new_id = uuid.uuid4().hex[:8]
        # Ensure the ID is unique
        while AdminDT.objects.filter(admin_id=new_id).exists():
            new_id = uuid.uuid4().hex[:8]
        return new_id