from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Order, LabBooking, Product

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'user_type', 'department', 'mobile_number')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'discounted_price', 'image', 'stock']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['quantity', 'customization_text', 'customization_font', 'customization_image']

    def __init__(self, *args, **kwargs):
        product_category = kwargs.pop('product_category', None)
        super().__init__(*args, **kwargs)
        
        if product_category in ['TSHIRT', 'CUP']:
            #self.fields['customization_text'].required = False
            #self.fields['customization_font'].required = False
            self.fields['customization_image'].required = False
        elif product_category in ['3DPRINT', 'WOODCARVE']:
            #self.fields['customization_text'].required = False
            #self.fields['customization_font'].required = False
            self.fields['customization_image'].required = False


from django import forms
from .models import LabBooking

class LabBookingForm(forms.ModelForm):
    class Meta:
        model = LabBooking
        fields = ['event_name', 'event_coordinator', 'chief_guest', 
                 'chief_guest_designation', 'lab', 'start_date', 
                 'end_date', 'event_description']
        widgets = {
            'event_name': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'
            }),
            'event_coordinator': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'
            }),
            'chief_guest': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'
            }),
            'chief_guest_designation': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'
            }),
            'lab': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'
            }),
            'start_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'
            }),
            'end_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'
            }),
            'event_description': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'rows': 3
            })
        }



from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            }),
            'description': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'rows': 4
            }),
            'price': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            }),
            'image': forms.FileInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            }),
            'category': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            }),
        }
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'user_type', 'department', 'mobile_number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            })


# forms.py
from django import forms
from .models import CustomUser, Product

class CustomUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'user_type', 'department', 'mobile_number', 'status']
        
    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'discounted_price', 'image', 'stock']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }