from django.shortcuts import render
from .models import *
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
from django.db.models import Avg,Sum,Value
from order.models import order
from inventory.models import product
from user.models import user_registration
from django.db.models import Q
from django.db.models.functions import Coalesce
# Create your views here.

# login Page view
def loginpageview(request):
    try:
        # Applied cookie 
        if request.COOKIES.get("username") and request.COOKIES.get("password"):
            username=request.COOKIES.get("username")
            password=request.COOKIES.get("password")
            return render(request,"user/login2.html",{"username":username,"password":password,"chk":"checked"})
        else:
            username=request.COOKIES.get("username")
            password=request.COOKIES.get("password")
            return render(request,"user/login2.html")
    except Exception as e:
        return HttpResponse(f"Error occured {e} ")


# registration page
def registerpageview(request):
     try:
        error={
            "firstname":[],
            "lastname" :[],
            "password":[],
            "username":[]

        }

        if request.method=="POST":
            # Applied validation on registration page

            firstname=request.POST['fname']
            if str(firstname).strip()=="":
                error["firstname"].append("firstname not empty")
            if len(str(firstname))<2:
                error["firstname"].append("enter firstname length beetween 2 and 12 ")
            if str(firstname).isdigit():
                error["firstname"].append("firstname contain mixing of number and character")

            lastname=request.POST['lname']
            if str(lastname).strip()=="":
                error["lastname"].append("lastname not empty")
            if len(str(lastname))<2:
                error["lastname"].append("enter lastname length beetween 2 and 12 ")
            if str(lastname).isdigit():
                error["lastname"].append("lastname contain mixing of number and character")

            username=request.POST['username']
            if str(username).strip()=="":
                error["username"].append("username not empty")
            if len(str(lastname))<2:
                error["username"].append("enter username length beetween 2 and 12 ")
            if str(lastname).isdigit():
                error["username"].append("username contain mixing of number and character")

            password=request.POST['password']
            if str(password).strip()=="":
                error["password"].append("password not empty")
            if len(str(password))<2:
                error["password"].append("enter password length beetween 2 and 8 ")
            if str(password).isdigit():
                error["password"].append("password contain mixing of number and character")
            if not(str(password).isalnum()):
                error["password"].append("password contain mixing of number and character") 
            data={
                "firstname":firstname,
                "lastname":lastname,
                "username":username,
                "password":password      
            }
        
            if error['firstname']!=[] or error["lastname"]!=[] or error["password"]!=[] or error["username"]!=[]:
                return render(request,"user/register2.html",{"error":error,"data":data})
            else:
                if user_registration.objects.filter(username=username).exists():
                    messages.info(request,f"user {username} already exist")
                    return render(request,"user/register2.html",{"data":data})
                else:
                    user=user_registration.objects.create(
                        first_name=firstname,
                        last_name=lastname,
                        username=username,
                        password=make_password(password))
                    messages.success(request,f"User {username} registered succesfully !!!")
                    return render(request,"user/register2.html")
        else:
            return render (request,"user/register2.html")
        
     except Exception as e:
        return HttpResponse(f"Error occured {e} ")


# login validation
def loginvalidation(request):
     try:
        if request.method=="POST":
            username=request.POST['username']
            password=request.POST['password']
            user=authenticate(request,username=username,password=password)
            if user:
                if user.is_superuser:
                    login(request,user)
                    response=redirect("inventory")
                    if request.POST.get("chk"):
                        response.set_cookie("username",user.username,max_age=60*60*24)
                        response.set_cookie("password",password,max_age=60*60*24)
                        print(request.user)
                        return response
                    else:
                        response.delete_cookie("username")
                        response.delete_cookie("password")
                        return response
                else:
                    login(request,user)
                    response=redirect("cusomerorder")
                    print(request.user)
                    if request.POST.get("chk"):
                        response.set_cookie("username",user.username,max_age=60*60*24)
                        response.set_cookie("password",password,max_age=60*60*24)
                        return response
                    else:
                        response.delete_cookie("username")
                        response.delete_cookie("password")
                        return response
                    
            else:
                    messages.error(request,"invalid credentials")
                    return render(request,"user/login2.html",{"data":{
                    "username": username,
                        "password":password
                }})
        else:
            return redirect("login")
         
     except Exception as e:
        return HttpResponse(f"Error occured {e} ")

      
# base page view 
@login_required
def baseview(request):
    return render(request,"user/base.html")


# log out user 
@login_required
def logoutuser(request):
    logout(request)
    return redirect("login")

# dashboard url
@login_required
def dashboard(request):
    try:
        # show recent order 
        recent_order=order.objects.all().order_by( "-id" )[:3]

        # Total customer count
        customercount=user_registration.objects.filter(is_staff ="0").count()

        # Total order count
        order_count=order.objects.all().count()

        # Total expenses
        total_qunatity = product.objects.all().aggregate(Sum("quantity_in_stock"))
        l=[]
        for i in product.objects.all():
            count=i.quantity_in_stock*i.selliing_price
            l.append(count)

        inventory=product.objects.filter(Q(quantity_in_stock__gt=0 ) and  Q(quantity_in_stock__lt=3))
        
        # Top selling     
        t=[]
        top_selling=order.objects.filter(status="1")
        for  i in top_selling:
            d={"id":i.product_name.id,"quantity":i.quantity}
            t.append(d)
        
        w={ }
        for j in t:
            id=j['id']
            quantity=j['quantity']
            if id in w:
                w[id]+= quantity
            else:
                w[id]= quantity
    
        
        sort_d={k:v for k,v in sorted(w.items(),key=lambda w:w[1],reverse=True)}
       
        s=list(sort_d.items())
        top_selling2=[]
        for i in s[:3]:
            qu=i[1]
            n=product.objects.get(id=i[0])
            j={"name":n.product_name,"sold":qu,"price":n.selliing_price}
            top_selling2.append(j)
                                        
        # quantity in stock
        default_value=0
        instock = product.objects.aggregate(total_stock=Coalesce(Sum("quantity_in_stock"), Value(default_value)))
    
        # Total revenue
        total_revenue=order.objects.filter(status="1")
        revenue=[]
        for i in total_revenue:
            r=i.product_name.selliing_price-i.product_name.cost_price
            revenue.append(r)
        
        context={"dashboard":"active","recent_orders":recent_order,"customer_count":customercount,"order_count":order_count,"total_qunatity":total_qunatity,"total_expenses":sum(l),"inventory":inventory,"top_selling":top_selling2,"revenue":sum(revenue),'instock':instock}

        return render(request,"user/dashboard.html",context)
    
    except Exception as e:
        return HttpResponse(f"Error occured : {e} ")