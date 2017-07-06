from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .forms import RegistrationForm, DocumentForm, ProductForm
from django.core.mail import send_mail
from .models import Document, Product
from tasks import file_upload,send_email
from helper import Helper
import time
#from celery import jobs

from Repricer import settings

from .Toolbox import Toolbox
tlbx = Toolbox()

def index(request):
    """Test"""
    if 'user' in request.session and request.session['user'] is not None:
        return redirect('../profile/')
    return redirect('../login/')

def registration(request):
    '''Register a user'''
    if 'user' in request.session and request.session['user'] is not None:
        return redirect('../profile/')
    tlbx.validateRequest(request)
    context = tlbx.getStandardContext(request)
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            print(form.cleaned_data)
            request.session['user']=form.cleaned_data['registerusername']
            return redirect('../profile/')
        else:
            context['form'] = form
            return render(request, "newegg/registration_form.html",context)
    return render(request, "newegg/registration_form.html",context)

def login_v(request):
    '''Login a user'''
    if 'user' in request.session and request.session['user'] is not None:
        return redirect('../profile/')
    tlbx.validateRequest(request)
    context = tlbx.getStandardContext(request)
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password1']

        try:
            #note to self, check this part out later
            if '@' in username:
                username=User.objects.get(email=username).username
        except User.DoesNotExist:
            context['form']='email is invalid'
            return render(request, 'newegg/login.html', context)

        try:
            findUser = User._default_manager.get(username__iexact=username)
        except User.DoesNotExist:
            findUser = None
        user = authenticate(username=findUser.username, password=password)
        if user is not None:
            print(user.is_active)
            if user.is_active:
                request.session['user'] = user.username
                login(request, user)
            return redirect('../profile/')
        else:
            context['form'] = 'user credentials are invalid'
            return render(request, 'newegg/login.html', context)
    return render(request, 'newegg/login.html',context)

def logout(request):
    '''Logout the user'''
    request.session['user'] = None
    return redirect('../login/')


def profile(request):
    '''go to profile'''
    if 'user' not in request.session or request.session['user'] is None:
        return redirect("../login/")
    tlbx.validateRequest(request)
    context = tlbx.getStandardContext(request,User)
    print(context)
    products_tracked = Product.objects.filter(client_id=context['auth_user_id'],is_active=True)
    print(products_tracked)#note fix price updating when typing

    context['tracked']=products_tracked

    return render(request, 'newegg/profile.html',context,status=200)

def model_form_upload(request):
    '''upload a model'''

    #issue 22 fix. If the user is not logged in, the page will crash.
    #changes should be below the 2 if conditionals.

    #if the user is not logged in, redirect them to the login screen
    tlbx.validateRequest(request)
    context = tlbx.getStandardContext(request,User)

    #after this point, testing and usual updates are possible.

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():

            #file = Document(description=description,document=document,client_id=2)
            form.save(request.session['user'], request.FILES['myFile'])#must pick a user with valid clients
            return redirect('../profile/')
        else:

            context['form']=form
            return render(request, 'newegg/file_upload.html', context)
    else:
        form = DocumentForm()
        context['form']=form
        return render(request, 'newegg/file_upload.html', context)
    return render(request, 'newegg/file_upload.html',context,status=200)

def products(request):
    '''track products'''

    #issue 22 fix. If the user is not logged in, the page will crash.
    #changes should be below the 2 if conditionals.

    #if the user is not logged in, redirect them to the login screen
    tlbx.validateRequest(request)
    context = tlbx.getStandardContext(request,User)

    user_products = Product.objects.filter(client_id=context['auth_user_id'])
    user_products_title = user_products.values_list('title', flat=True)
    user_products_title_ordered = user_products_title.order_by('title')

    if request.method == 'POST':
        form = ProductForm(request.POST)
        user_products = Product.objects.filter(client_id=context['auth_user_id'])
        user_products_title = user_products.values_list('title', flat=True)
        user_products_title_ordered = user_products_title.order_by('title')

        p_mins=request.POST.getlist('product_min')
        p_maxs=request.POST.getlist('product_max')



        prod_new_min={}
        prod_new_max={}
        for title,p_min_price,p_max_price in zip(user_products.values_list('title',flat=True),p_mins,p_maxs):
            prod_new_min.update({title:p_min_price})
            prod_new_max.update({title:p_max_price})


        if form.is_valid():
            form.save(request.session['user'],prod_new_min,prod_new_max)
            return redirect('../products/')
        else:
            print(form.errors)
            form = ProductForm()

        context['form']=form
        context['product']=user_products
        return render(request, 'newegg/product_toggle.html', context)

    context['products']=user_products_title_ordered
    context['product']=user_products
    return render(request, 'newegg/product_toggle.html', context)
