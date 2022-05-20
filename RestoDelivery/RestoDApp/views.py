from sys import platlibdir
from unicodedata import category
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.views import View
from django.template.loader import render_to_string
from .models import *
import random


def search(request):
    type=request.GET.get('categorie')
    if not type:
        plat = Plat.objects.all()
    else:
        plat = Plat.objects.filter(nom__icontains=type)
    if not plat:
        plat = Plat.objects.filter(id_ga__Name_gam__icontains=type)
       

    nbr=plat.count()
    p= Paginator(plat,6)
    page = request.GET.get('page')
       
    try:
        result = p.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        result = p.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        result = p.page(p.num_pages)

    context={
        'plat': result,
        'type': type,
        'nbr':nbr,
        'paginate': True
    }
    return render(request, '', context)

class IndexView(View):
    def get(self,request):
        plat=Plat.objects.all()[:3]
        return render(request,'',{'plat':plat})

class AboutView(View):
    def get(self,request):
        return render(request,'')

class PlatView(View):
    def get(self,request,type):
        categorie="None"
        
        if categorie=="All products":
            plat=Plat.objects.all()

        elif categorie=="":
            plat=Plat.objects.filter(id_cat=Categorie.objects.get(nom=type))
        
        
        nbr=plat.count()
        p= Paginator(plat,6)
        page = request.GET.get('page')
       
        try:
            result = p.page(page)
        except PageNotAnInteger:
        # If page is not an integer, deliver first page.
            result = p.page(1)
        except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
            result = p.page(p.num_pages)

        if not plat:
            return  render(request,'',{})
        
        
        context={
            'plat':result,
            'categorie':categorie,
            'nbr':nbr,
            'paginate': True
        }
        return render(request,'',context)

        

class ContactView(View):
    def get(self,request):
        return render(request,'')


class PlatDetailView(View):
    def get(self,request,plat_id):
        plat=Plat.objects.get(pk=plat_id)
        categorie=Categorie.objects.get(Name_cat=plat.id_cat)
        randomnumber=random.randint(1, Plat.objects.count()-4)
        context={
            'plat':plat,
            'categorie':categorie,
            'relatedprod':Plat.objects.all()[randomnumber:randomnumber+4]
        }
        return render(request,'',context)

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
            return render(request, '',context)
        except KeyError:
            return render(request, '',{'total_amt':total_amt,'totalitems':0})

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