from django.shortcuts import render, redirect
from .models import Product
from .forms import ProductForm

# Create your views here.
# CRUD = Create, Read, Update, Delete

def home_view(request):
    return render(request, 'invApp/home.html')

# Create a view to list all products
def product_list_view(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'invApp/product_list.html', context)

# Create a view to create a new product
def product_create_view(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        # form = ProductForm()
        return redirect('product_list')
    context = {
        'form': form
    }
    return render(request, 'invApp/product_form.html', context)
# the above code can also be written as:
# if request.method == 'POST':
#     form = ProductForm(request.POST)
#     if form.is_valid():
#         form.save()
#         form = ProductForm()
# else:
#     form = ProductForm()
# context = {
#     'form': form
# }
# return render(request, 'invApp/product_create.html', context)


# Create a view to update a product
def product_update_view(request, product_id):
    product = Product.objects.get(product_id=product_id)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('product_list')
    context = {
        'form': form
    }
    return render(request, 'invApp/product_form.html', context)

# Create a view to delete a product
def product_delete_view(request, product_id):
    product = Product.objects.get(product_id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    context = {
        'object': product
    }
    return render(request, 'invApp/product_confirm_delete.html', context)
