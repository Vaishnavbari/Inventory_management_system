from django.shortcuts import render
from inventory.models import *
from order.models import order
from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.db.models import Avg,Sum
from django.core.paginator import Paginator
from django.db.models import Q
import json
# Create your views here.

# inventory page view
@login_required
def inventory(request):
   try:
        # pagination 
        all_product=product.objects.all().order_by('id')
        page=Paginator(all_product,5)
        page_number=request.GET.get('page')
        page_obj=page.get_page(page_number)
        
        # Count total quantity
        total_quantity=product.objects.aggregate(Sum("total_quantity"))
    
        # Total quantity in stock
        quantity_in_stock=product.objects.aggregate(Sum("quantity_in_stock"))
        
        # low in stock product 
        low_in_stock=product.objects.filter(quantity_in_stock__lt=20)
        low_quantity_in_stock=low_in_stock.aggregate(Sum('quantity_in_stock'))

        context={"category":category.objects.all(),"product":page_obj,"total_quantity":total_quantity,"inventory":"active","in_stock":quantity_in_stock ,"low_in_stock":low_quantity_in_stock}

        return render(request,"app/inventory.html",context)
   except Exception as e:
        return HttpResponse(f"Error occured {e} ")


# add inventory form
@login_required
def add_inventory_form(request):
    try:
        error={
            "product_name":[],
            "product_category":[],
            "selling_price":[],
            "cost_price":[],
            "quantity":[],
            "short_description":[],
            "detail_description":[],
            "image":[],
        }

        # Applied validation on add inventory 
        if request.method=="POST":
            product_name=request.POST['pname']
            if product_name=="":
                error["product_name"].append("product name not empty")

            try:
                product_category=request.POST['pcategory']
                p=category.objects.get(name=product_category)
            except:
                error["product_category"].append("please select category")
            
            
            selling_price=request.POST['sprice']
            
            if selling_price=="":
                error["selling_price"].append("selling price not null")
            if not(str(selling_price).replace(".","",1).isdigit()):
                error["selling_price"].append("please enter only number")

            cost_price=request.POST['cprice']
            
            if cost_price=="":
                error["cost_price"].append("cost price not null")
            if not(str(cost_price).replace(".","",1).isdigit()):
                error["cost_price"].append("please enter only number")

            quantity=request.POST['quantity']
            if quantity=="":
                error["quantity"].append("quantity not null")
            if not(str(quantity).replace(".","",1).isdigit()):
                error["quantity"].append("please enter only number")
                
            short_description=request.POST['sd']
            if short_description=="":
                error["short_description"].append("short description not null ")
            detail_description=request.POST['dd']
            
            try:
                images=request.FILES['file']
            except:
                error['image'].append("please select image ")


            if error["product_name"]!=[] or error["selling_price"]!=[] or error["product_category"]!=[] or error["cost_price"]!=[] or error["quantity"]!=[] or error["image"]!=[] or error["short_description"]!=[]:
                print("if block")
                return render(request,"app/add_inventory2.html",{"error":error,"category":category.objects.all(),"product_name":product_name,"selling_price":selling_price,"cost_price":cost_price,"quantity":quantity,"sdescription":short_description,"ldescription":detail_description})
            else:
                p=product.objects.create(product_name=product_name.strip(),product_category=p, selliing_price=selling_price,cost_price=cost_price,quantity_in_stock=quantity,short_description=short_description,detail_description=detail_description,total_quantity=quantity)
                image.objects.create(image=images,product_id=p)
                messages.success(request,"inventory add succesfully")
                return render(request,"app/add_inventory2.html",{"category":category.objects.all()})
                
        else:
            return render(request,"app/add_inventory2.html",{"category":category.objects.all()})
    except Exception as e:
        return HttpResponse(f"Error occured {e} ")


# delete product
@login_required
def deleteproduct(request,id):
    try:
        pro=product.objects.get(id=id)
        pro.delete()
        return redirect("inventory")
    except Exception as e:
        return HttpResponse(f"Error occured {e} ")


# view inventory 
@login_required
def viewinventory(request,id):
    try:
        # Show product details
        prod=product.objects.get(id=id)
        purchase_history=order.objects.filter(product_name=id)
        count = purchase_history.count()

        # Sold product count
        sold_count=order.objects.filter(product_name=id).filter(status="1")
        sold=sold_count.aggregate(Sum('quantity'))
        
        # Show image on view page 
        Get_image=image.objects.filter(product_id=prod.id)

        return render(request,"app/view.html",{"product":prod,"image":Get_image,"purchase":purchase_history,"count":count,"sold":sold})
    
    except Exception as e:
        return HttpResponse(f"Error occured {e} ")


# Edit inventory 
@login_required
def editinventory(request,id): 
    try:
        # Applied validation on edit inventory 

        pro=product.objects.get(id=id)
        i=image.objects.filter(product_id=pro.id)
        error={
            "product_name":[],
            "product_category":[],
            "selling_price":[],
            "cost_price":[],
            "quantity":[],
            "short_description":[],
            "detail_description":[],
            "image":[],

            }
        if request.method=="POST":
            
            pro.product_name=request.POST['pname']
            if pro.product_name=="":
                error["product_name"].append("product name not empty")

            product_category=request.POST['pcategory']
            
            pro.product_category=category.objects.get(name=product_category)
            p_id=product.objects.get(id=pro.id)
            pro.selliing_price=request.POST['sprice']
            print(pro.selliing_price)
            if pro.selliing_price=="":
                error["selling_price"].append("selling price not null")
            if not( str(pro.selliing_price).replace(".","",1).isdigit()):
                error["selling_price"].append("please enter only number")
            print(pro.selliing_price)
            
            pro.cost_price=request.POST['cprice']
            if pro.cost_price=="":
                error["cost_price"].append("cost price not null")
            if not(str(pro.cost_price).replace(".","",1)):
                error["cost_price"].append("please enter only number")
                
            pro.quantity_in_stock=request.POST['quantity']
            if pro.quantity_in_stock=="":
                error["quantity"].append("quantity not null")
            if not(str(pro.quantity_in_stock).replace(".","",1).isdigit()):
                error["quantity"].append("please enter only number")

            pro.short_description=request.POST['sd']
            if pro.short_description=="":
                error["short_description"].append("short description not null ")
        
            pro.detail_description=request.POST['dd']
        
            for v in request.FILES.getlist('file'):
                imageinstanvce=image.objects.create(image=v,product_id=p_id)
        
            if error["product_name"]!=[] or error["selling_price"]!=[] or error["product_category"]!=[] or error ["cost_price"]!=[] or error["quantity"]!=[] or error["image"]!=[] or error["short_description"]!=[]:
                return render(request,"app/edit_inventory2.html",{"error":error,"pro":pro,"image":i})
            else:
                pro.save()
                messages.success(request, "inventory update succesfully ")
                return render(request,"app/edit_inventory2.html",{"category":category.objects.all(),"pro":pro,"image":i})
        else:
            return render(request,"app/edit_inventory2.html",{"pro":pro,"image":i,"category":category.objects.all()})
        
    except Exception as e:
        return HttpResponse(f"Error occured {e} ")

    

# image delete view
@login_required
def imagedeleted(request,id):
    try:
        delete_image=image.objects.get(id=id)
        delete_image.delete()
        return HttpResponse("image deleted successfully ")
    except Exception as e:
        return HttpResponse(f"Error occured {e} ")


@login_required
def check_product_exist(request,name):
   try:
        product_exist=product.objects.filter(product_name=name).exists()
        if product_exist:
            return JsonResponse({"true":"true"})
        else:
            return HttpResponse("Product not exist ")
   except Exception as e:
        return HttpResponse(f"Error occured {e} ")




@login_required
def search_inventory_content(request,selectedValue=None):
    try:
        all_data=product.objects.all().values()
        if selectedValue:
            all_data=all_data.filter(product_name__icontains=selectedValue)
            
        return JsonResponse({"data":list(all_data)})
        
    except Exception as e:
        return HttpResponse(f"Error occured {e} ")



@login_required
def search_view_content(request,selectedValue=None):
    try:
        all_data=order.objects.all()
        
        if selectedValue:
            all_data=all_data.filter(product_name__product_name__icontains=selectedValue)
            
        return render(request,"app/table.html",{"purchase":all_data})
        
    except Exception as e:
        return HttpResponse(f"Error occured {e} ")