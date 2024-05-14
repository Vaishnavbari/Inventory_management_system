from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from inventory.models import category,product
from order.models import order
from datetime import datetime
from random import randint
from django.contrib import messages
from django.db.models import Count
from django.core.paginator import Paginator
# Create your views here.

# order page view 
@login_required
def orderview(request):
    try:
        # Get all order count 

        all=order.objects.all().order_by('id')
        all_order_count=order.objects.aggregate(Count("id"))

        # Count pending details
        pending=order.objects.filter(status=0)
        pending_count=pending.count()

        # Count completed details
        completed=order.objects.filter(status=1)
        completed_count=completed.count()

        # Count cancel  details
        cancel=order.objects.filter(status=4)
        cancelled=cancel.count()

        # Count cancel  details
        damage=order.objects.filter(status=3)
        damaged=damage.count()

        # Count cancel  details
        returned=order.objects.filter(status=2)
        c_returned=returned.count()

        # Applied pagination 
        page=Paginator(all,5)
        page_number=request.GET.get('page')
        page_obj=page.get_page(page_number)

        return render(request,"order/order.html",{"order":"active","product":page_obj,"all_order_count":all_order_count,"pending":pending_count,"completed":completed_count,"cancel":cancelled,"return":c_returned,"damaged":damaged})

    except Exception as e:
        return render("500page")


# add order 
@login_required
def addorder(request):
    try:
        if request.method=="POST":
            # Get Order details from customer 
            product_name=request.POST["product"]
            d=product.objects.get(id=product_name)
            quantity=request.POST['Quantity'] 
            order_total=request.POST['price']
            tracking_id=randint(1999999999991,90000000000000000)
            order.objects.create(customer_name=request.user,product_name=d,quantity=quantity,order_date=datetime.now(),tracking_id=tracking_id,order_total=order_total)
            messages.success(request,"your order send succesfully ")
            return render(request,"order/add_order.html")
        else:
            return render(request,"order/add_order.html",{"category":category.objects.all(),"product":product.objects.all()})
        
    except Exception as e:
        return render("500page")


# customer order page 
@login_required
def customer_order_page(request):
    try:
         myorder=order.objects.filter(customer_name=request.user.id).order_by( '-id' )

         #Applied pagination 
         page=Paginator(myorder,5)
         page_number=request.GET.get('page')
         page_obj=page.get_page(page_number)

         return render(request,"order/customeroreder.html",{"order":"active","product":page_obj})
    except Exception as e:
         return render("500page")
   

@login_required
def show_selected_product(request,id):
    try:
        c=product.objects.filter(product_category=id)
        x=[]
        for i in c:
            g={"poduct_id":i.id,"product_name":i.product_name}
            x.append(g)
        return JsonResponse({"x":x})
    except Exception as e:
        return render("500page")


# count price
@login_required
def count_price(request,id,quantity):
    try:
        # count price of product
        c=product.objects.get(id=id)
        x=c.selliing_price*quantity
        return JsonResponse({"x":x})
    except Exception as e:
        return render("500page")



@login_required
def statuscompletedurl(request,id,selected_value):
        try:
            y=order.objects.get(id=id)
            if selected_value=="1":
                if y.product_name.quantity_in_stock>= y.quantity:
                    qunatity=y.product_name.quantity_in_stock- y.quantity
                    y.product_name.quantity_in_stock=qunatity
                    y.product_name.save()
                    y.status="1"
                    y.save()
                    return JsonResponse({"y":"false"})
                else:
                    return JsonResponse({"y":"true"})
            elif selected_value=="2":
                y.status="2"
                y.save()
                return redirect('cusomerorder')
            elif selected_value=="3":
                y.status="3"
                y.save()
                return redirect('cusomerorder')
            elif selected_value=="4":
                y.status="4"
                y.save()
                return redirect('cusomerorder')
        except :
            return render("500page")


@login_required
def quantityvalidtaion(request,id,quantity):
    try:
        p=product.objects.get(id=id)
        
        if p.quantity_in_stock<quantity:
            return JsonResponse({"true":"true"})
        else:
            return JsonResponse({"false":"false"})  
    except Exception as e:
       return render("500page")
    

# @login_required
# def search_order_content(request,selectedValue=None):
#     try:
#         all_data=order.objects.all()
#         if selectedValue:
#             all_data=all_data.filter(product_name__product_name__icontains=selectedValue)
#         print(all_data)
#         return render(request,"order/table2.html",{"product":all_data})
        
#     except Exception as e:
#         return render("500page")
    

@login_required
def search_order_content_view(request,selectedValue=None):
    try:
        all_data=order.objects.all()
        
        if selectedValue:
            all_data=all_data.filter(product_name__product_name__icontains=selectedValue)
            
        return render(request,"order/table3.html",{"product":all_data})
        
    except Exception as e:
        return render("500page")