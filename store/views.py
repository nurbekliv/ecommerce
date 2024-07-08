from django.shortcuts import render, redirect
from cart.cart import Cart
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from store.forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django.contrib.auth import update_session_auth_hash  # Keeps the user logged in after password change
from django.db.models import Q
import json

from payment.forms import ShippingForm
from payment.models import ShippingAddress


# Search function to find products
def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        products = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        context = {'products': products, 'searched': searched}
        if not searched:
            messages.error(request, 'No products found')
            return render(request, 'search.html', context)
        else:
            return render(request, 'search.html', context)
    else:
        return render(request, 'search.html', {})


# Function to update user information
def update_info(request):
    if request.user.is_authenticated:
        try:
            current_user = Profile.objects.get(user__id=request.user.id)
        except Profile.DoesNotExist:
            messages.error(request, 'Profile does not exist. Please contact support.')
            return redirect('home')

        try:
            shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        except ShippingAddress.DoesNotExist:
            messages.error(request, 'Shipping address does not exist.')
            shipping_user = None

        form = UserInfoForm(request.POST or None, instance=current_user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        if form.is_valid() and (shipping_user is not None and shipping_form.is_valid()):
            form.save()
            shipping_form.save()
            messages.success(request, 'Your info has been updated!')
            return redirect('home')

        return render(request, 'update_info.html', {'form': form, 'shipping_form': shipping_form})
    else:
        messages.success(request, 'You must be logged in to access this page')
        return redirect('home')


# Function to update user password
def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)  # Keeps the user logged in
                messages.success(request, 'Your password has been updated!')
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form': form})
    else:
        messages.success(request, 'You must be logged in to view this page')
        return redirect('home')


# Function to update user account information
def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, 'Your account has been updated!')
            return redirect('home')
        return render(request, 'update_user.html', {'user_form': user_form})
    else:
        messages.success(request, 'You must be logged in to access this page')
        return redirect('home')


# Function to show category summary
def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {'categories': categories})


# Function to show products in a specific category
def category(request, foo):
    foo = foo.replace('-', ' ')
    try:
        kategory = Category.objects.get(name=foo)
        products = Product.objects.filter(category=kategory)
        return render(request, 'category.html', {'products': products, 'category': kategory})
    except:
        messages.success(request, "That category does not exist")
        return redirect('home')


# Function to show details of a specific product
def product(request, pk):
    products = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': products})


# Home page view
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


# About page view
def about(request):
    return render(request, 'about.html', {})


# Function to log in a user
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user = Profile.objects.get(user__id=request.user.id)
            saved_cart = current_user.old_cart
            if saved_cart:
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)
            messages.success(request, 'You are now logged in')
            return redirect('home')
        else:
            messages.success(request, 'There was an error, please try again')
            return redirect('login')
    else:
        return render(request, 'login.html', {})


# Function to log out a user
def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


# Function to register a new user
def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Username created, please fill out your user info below')
                return redirect('update_info')
            else:
                messages.error(request, 'There was a problem logging in after registration.')
                return redirect('register')
        else:
            # Reload the form with errors if any
            messages.error(request, 'There was a problem with your registration.')
    return render(request, 'register.html', {'form': form})
