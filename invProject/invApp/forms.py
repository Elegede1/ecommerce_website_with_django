from django import forms
from.models import Product

class ProductForm(forms.ModelForm):
    class Meta: # Meta class is used to define the model and fields that will be used in the form.
        model = Product
        fields = '__all__' # this can also be written as fields = ['name', 'sku', 'price', 'quantity', 'supplier']
        labels = {
            'product_id': 'Product ID',
            'name': 'Product Name',
            'sku': 'SKU',
            'price': 'Price',
            'quantity': 'Quantity',
            'supplier': 'Supplier'
        }
        widgets = { # this is used to add bootstrap classes to the form fields.
            'product_id': forms.NumberInput(attrs={'placeholder': 'e.g. 1', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'placeholder': 'e.g. Laptop', 'class': 'form-control'}),
            'sku': forms.TextInput(attrs={'placeholder': 'e.g. LAPTOP123', 'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'placeholder': 'e.g. 999.99', 'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'placeholder': 'e.g. 10', 'class': 'form-control'}),
           'supplier': forms.TextInput(attrs={'placeholder': 'e.g. Acer', 'class': 'form-control'})
        }