from sys import platlibdir
from unicodedata import category
from django.shortcuts import render, redirect,get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.views import View
from django.template.loader import render_to_string
from .models import *
import random
from django.contrib import messages
from RestoDApp.forms import *
from .decorators import *


def register(request):

    form=CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request,'Account was created for'+username)
            return redirect('login')
    
    context={
        'form':form,
    }
    return render(request,'account/register.html',context)

def Login(request):
    if request.method == 'POST':
        username= request.POST.get('username')
        password= request.POST.get('password')
        user=authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('IndexView')
            
    return render(request,'account/login.html')

def Logout(request):
    logout(request)
    return redirect('IndexView')

def search(request):
    type=request.GET.get('type')
    if not type:
        menu = MenuItem.objects.all()
    else:
        menu = MenuItem.objects.filter(category__nom=type)

    context={
        'menu': menu,
        'type': type,
    }
    return render(request, 'store/menu.html', context)

class IndexView(View):
    def get(self,request):
        resto=Restaurant.objects.all()
        return render(request,'store/index.html',{'resto':resto})

class AboutView(View):
    def get(self,request):
        return render(request,'store/about.html')

class ContactView(View):
    def get(self,request):
        return render(request,'store/ContactUs.html')

class RestoView(View):
    def get(self,request,categorie):
        
        if categorie=="All":
            resto=Restaurant.objects.all()

        elif categorie=="":
            resto=Restaurant.objects.filter(id_cat=Categorie.objects.get(nom=type))
        
        
        nbr=resto.count()
        p= Paginator(resto,6)
        page = request.GET.get('page')
       
        try:
            resto = p.page(page)
        except PageNotAnInteger:
        # If page is not an integer, deliver first page.
            resto = p.page(1)
        except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
            resto = p.page(p.num_pages)

        if not resto:
            return  render(request,'store/resto.html',{})
        
        
        context={
            'resto':resto,
            'categorie':categorie,
            'nbr':nbr,
            'paginate': True
        }
        return render(request,'store/resto.html',context)

        


class MenuView(View):
    def get(self,request,categorie):
        
        if categorie=="All":
            menu=MenuItem.objects.all()

        else:
            menu=MenuItem.objects.filter(id_cat=Categorie.objects.get(nom=categorie))
        
        
        nbr=menu.count()
        p= Paginator(menu,6)
        page = request.GET.get('page')
       
        try:
            menu = p.page(page)
        except PageNotAnInteger:
        # If page is not an integer, deliver first page.
            menu = p.page(1)
        except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
            menu = p.page(p.num_pages)

        if not menu:
            return  render(request,'store/index.html',{})
        
        
        context={
            'menu':menu,
            'categorie':categorie,
            'nbr':nbr,
            'paginate': True
        }
        return render(request,'store/menu.html',context)

        


class MenuDetailView(View):
    def get(self,request,menu_id):
        menu=MenuItem.objects.get(pk=menu_id)
        categorie=Categorie.objects.get(nom=menu.category)
        randomnumber=random.randint(1, MenuItem.objects.count())

        context={
            'menu':menu,
            'categorie':categorie,
            'relatedprod':MenuItem.objects.all()[randomnumber:randomnumber+4]
        }
        return render(request,'store/shop-details.html',context)

class addTocart(View):
    def get(self,request):
        
        cart_p={}
        cart_p[str(request.GET['id'])]={
		    'image':request.GET['image'],
		    'title':request.GET['title'],
		    'qty':request.GET['qty'],
		    'price':request.GET['price'],
	    }
        if 'cartdata' in request.session:
            if str(request.GET['id']) in request.session['cartdata']:
                cart_data=request.session['cartdata']
                cart_data[str(request.GET['id'])]['qty']=int(cart_p[str(request.GET['id'])]['qty'])
                cart_data[str(request.GET['id'])]['price']=float(cart_p[str(request.GET['id'])]['price'])
                cart_data.update(cart_data)
                request.session['cartdata']=cart_data
            else:
                cart_data=request.session['cartdata']
                cart_data.update(cart_p)
                request.session['cartdata']=cart_data
        else:
            request.session['cartdata']=cart_p
        return JsonResponse({'data':request.session['cartdata'],'totalitems':len(request.session['cartdata'])})

class ShoppingCartDetail(View):
    def get(self,request):
        total_amt=0
        try:
            for p_id,item in request.session['cartdata'].items():
                total_amt+=int(item['qty'])*float(item['price'])
            context={
                'items':request.session['cartdata'],
                'totalitems':len(request.session['cartdata']),
                'total_amt':total_amt,
            }
            return render(request, 'store/shopping-cart.html',context)
        except KeyError:
            return render(request, 'store/shopping-cart.html',{'total_amt':total_amt,'totalitems':0})

# Delete cart
def delete_cart_item(request):
	p_id=str(request.GET['id'])
	if 'cartdata' in request.session:
		if p_id in request.session['cartdata']:
			cart_data=request.session['cartdata']
			del request.session['cartdata'][p_id]
			request.session['cartdata']=cart_data
	total_amt=0
	for p_id,item in request.session['cartdata'].items():
		total_amt+=int(item['qty'])*float(item['price'])
	t=render_to_string('ajax/cart-list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
	return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})

# Update cart

def update_cart_item(request):
	p_id=str(request.GET['id'])
	p_qty=request.GET['qty']
	if 'cartdata' in request.session:
		if p_id in request.session['cartdata']:
			cart_data=request.session['cartdata']
			cart_data[str(request.GET['id'])]['qty']=p_qty
			request.session['cartdata']=cart_data
	total_amt=0
	for p_id,item in request.session['cartdata'].items():
		total_amt+=int(item['qty'])*float(item['price'])
	t=render_to_string('ajax/cart-list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
	return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})

@unauthenticated_user
def Checkout(request):
    return render(request,"store/checkout.html",{})