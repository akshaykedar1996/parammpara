# forms.py
from django import forms
from service.models import *

class CarouselImageForm(forms.ModelForm):
    class Meta:
        model = CarouselImage
        fields = ['title', 'image']


class FranchiseserviceForm(forms.ModelForm):
    class Meta:
        model = Franchiseservice
        fields = ['img1', 'title','paragraph','description','img2']
            

from django import forms


# class MainServiceForm(forms.ModelForm):
#     class Meta:
#         model = MainService
#         fields = ['title', 'image']

# class SubServiceForm(forms.ModelForm):
#     class Meta:
#         model = SubService
#         fields = ['main_service', 'title', 'image', 'description', 'faqs']

from django import forms

class MainServiceForm(forms.ModelForm):
    class Meta:
        model = MainService
        fields = ['title', 'image']
    
    def __init__(self, *args, **kwargs):
        super(MainServiceForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True  # ✅ sab field required ban gaye

class SubServiceForm(forms.ModelForm):
    class Meta:
        model = SubService
        fields = ['main_service', 'title', 'image', 'description', 'faqs']
    
    def __init__(self, *args, **kwargs):
        super(SubServiceForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True  # ✅ sab field required ban gaye


from django import forms

from django.core.validators import MaxLengthValidator

class TestimonialsForm(forms.ModelForm):
    class Meta:
        model = Testimonials
        fields = ['title', 'image', 'description1', 'post']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'required': 'required'}),
            'description1': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'maxlength': '300',   # For frontend HTML limit
                'required': 'required'
            }),
            'post': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'required': 'required'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Force required=True for all fields at form-level
        for field in self.fields.values():
            field.required = True

    def clean_description1(self):
        description = self.cleaned_data.get('description1')
        if len(description) > 300:
            raise forms.ValidationError("Description should not exceed 300 characters.")
        return description

from ecommerce.models import *

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = '__all__'

class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'image']

class ProductSubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['category', 'name', 'description', 'image']        