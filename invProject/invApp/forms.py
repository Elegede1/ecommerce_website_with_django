from django import forms
from.models import Product
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': 'Username',
            'email': 'Email',
            'password': 'Password',
        }
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password != password_confirm:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned_data

class ProductForm(forms.ModelForm):
    class Meta: # Meta class is used to define the model and fields that will be used in the form.
        model = Product
        fields = '__all__' # this can also be written as fields = ['name', 'sku', 'price', 'quantity', 'supplier']
        labels = {
            'product_id': 'Product ID',
            'name': 'Product Name',
            'sku': 'SKU', # SKU means Stock Keeping Unit.
            'price': 'Price',
            'quantity': 'Quantity',
            'supplier': 'Supplier',
            'image': 'Product Image',
        }
        widgets = { # this is used to add bootstrap classes to the form fields.
            'product_id': forms.NumberInput(attrs={'placeholder': 'e.g. 1', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'placeholder': 'e.g. Laptop', 'class': 'form-control'}),
            'sku': forms.TextInput(attrs={'placeholder': 'e.g. LAPTOP123', 'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'placeholder': 'e.g. 999.99', 'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'placeholder': 'e.g. 10', 'class': 'form-control'}),
           'supplier': forms.TextInput(attrs={'placeholder': 'e.g. Acer', 'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
