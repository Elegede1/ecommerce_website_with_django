from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm, UserForm
from .consumers import send_live_update
# to handle user registration
from django.contrib.auth import authenticate, login, logout
# to handle decorators to protect views
from django.contrib.auth.decorators import login_required
# for class-based views. LoginRequiredMixin is used to ensure that only authenticated users can access the views.
from django.contrib.auth.mixins import LoginRequiredMixin
# for class-based views. View is used to handle GET and POST requests.
from django.views import View
# to handle user registration
from django.contrib.auth.models import User
#  import authentificationform for login view
from django.contrib.auth.forms import AuthenticationForm


# Create your views here.

# Create a view to display the home page
def home_view(request):
    return render(request, 'invApp/home.html')

# Create a view to list all products
def product_list_view(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'invApp/product_list.html', context)

# Create a signup view
# Create a signup view
def signup_view(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # The form's save method (if it's a ModelForm that creates a user)
            # or manual user creation using cleaned_data
            user = form.save(commit=False)  # If UserForm is a ModelForm for User
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()

            # Log the user in directly after signup
            login(request, user)
            return redirect('home')  # Or to a profile page, or product_list
    else:
        form = UserForm()
    return render(request, 'invApp/signup.html', {'form': form})

# Create a login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password') # Not directly used, form handles auth
            user = form.get_user() # Get the authenticated user from the form
            if user is not None:
                login(request, user)
                return redirect('home') # Or to a profile page, or product_list
        # If form is not valid, it will fall through and re-render with errors
    else:
        form = AuthenticationForm()
    return render(request, 'invApp/login.html', {'form': form})

# Create a view to create a new product
@ login_required(login_url='/login/') # to protect the view from unauthenticated users
def product_create_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            product = form.instance
            message = f"Product {product.name} created successfully."
            payload = {
                'product_id': product.product_id,
                'name': product.name,
                'price': float(product.price),
                'image_url': product.image_url,
            }
            send_live_update(message, payload_data=payload)
            # form = ProductForm()
            return redirect('product_list')
    else:
        form = ProductForm()
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
@ login_required(login_url='/login/') # to protect the view from unauthenticated users
def product_update_view(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    if request.method == 'POST':
        product = Product.objects.get(product_id=product_id)
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            updated_product = form.instance
            message = f"Product {updated_product.name} updated successfully."
            payload = {
                'product_id': updated_product.product_id,
                'name': updated_product.name,
                'price': float(product.price),
                'image_url': updated_product.image_url,
            }
            send_live_update(message, payload_data=payload)
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    context = {
        'form': form,
        'product': product
    }
    return render(request, 'invApp/product_form.html', context)

# Create a view to delete a
@ login_required(login_url='/login/') # to protect the view from unauthenticated users
def product_delete_view(request, product_id):
    product = Product.objects.get(product_id=product_id)
    if request.method == 'POST':
        product_name = product.name
        product_image_url = product.image_url
        product.delete()
        message = f"Product {product_name} deleted successfully."
        payload = {
            'product_id': product_id, # product_id is still available
            'name': product_name,
            'action': 'deleted', # Add an action to help client-side logic
            'image_url': product_image_url # Send the old image_url or an indicator
        }
        send_live_update(message, payload_data=payload)
        return redirect('product_list')
    context = {
        'object': product
    }
    return render(request, 'invApp/product_confirm_delete.html', context)

# create view for logout
def logout_view(request):
    logout(request)
    return redirect('home')