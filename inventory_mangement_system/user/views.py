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
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
def page_404(request,exception):
    return render(request,"errorpage404.html", status=404)


def page_500(request):
    return render(request,"errorpage500.html",status=500)

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
        return redirect("500page")


# registration page
def registerpageview(request):
    try:
        error={
            "firstname":[],
            "lastname" :[],
            "password":[],
            "email":[],
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

            email=request.POST['email']
            if str(email).strip()=="":
                error["email"].append("Email not empty")
            if len(str(email))<2:
                error["email"].append("enter email length beetween 2 and 12 ")
            if str(email).isdigit():
                error["email"].append("email contain mixing of number and character")
            if not str(email).endswith("@gmail.com"):
                error["email"].append("enter valid email")


            password=request.POST['password']
            if str(password).strip()=="":
                error["password"].append("password not empty")
            if len(str(password))<2:
                error["password"].append("enter password length beetween 2 and 8 ")
            if str(password).isdigit():
                error["password"].append("password contain mixing of number and character")
            if not(str(password).isalnum()):
                error["password"].append("password contain mixing of number and character") 

            username=request.POST['username']
            if str(firstname).strip()=="":
                error["username"].append("username not empty")
            if len(str(firstname))<2:
                error["username"].append("enter username length beetween 2 and 12 ")
            if str(firstname).isdigit():
                error["username"].append("username contain mixing of number and character")

            data={
                "firstname":firstname,
                "lastname":lastname,
                "email":email,
                "password":password ,
                "username":username     
            }

            if error['firstname']!=[] or error["lastname"]!=[] or error["password"]!=[] or error["email"]!=[] or error['username']!=[]:
                return render(request,"user/register2.html",{"error":error,"data":data})
            else:
                if user_registration.objects.filter(email=email).exists():
                    messages.info(request,f"user {email} already exist")
                    return render(request,"user/register2.html",{"data":data})
                elif user_registration.objects.filter(username=username).exists():
                    messages.info(request,f"username {username} already exist")
                    return render(request,"user/register2.html",{"data":data})
                else:
                    user=user_registration.objects.create(
                        first_name=firstname,
                        last_name=lastname,
                        username=username,
                        email=email,
                        password=make_password(password))
                    messages.success(request,f"User {email} registered succesfully !!!")
                    return render(request,"user/register2.html")
        else:
            return render (request,"user/register2.html")
            
    except Exception as e:
        return redirect("500page")


# login validation
@csrf_exempt
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
    try:
      return render(request,"user/base.html")
    except Exception as e:
        return redirect("500page")


# log out user 
@login_required
def logoutuser(request):
    try:
        logout(request)
        return redirect("login")
    except Exception as e:
        return redirect("500page")

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
        return redirect("500page")


def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get('email')
        user = user_registration.objects.filter(email=email).first()
        if user:
            # Generate a password reset token
            token = default_token_generator.make_token(user)
            # Encode the user's primary key (usually the user ID)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            # Construct the password reset link
            password_reset_url = f"http://127.0.0.1:8000/password_request_confirm/{uid}/{token}"
           
            # Construct the password reset email
            email_subject = 'Password Reset Request'
            email_body = render_to_string('user/password_reset_email.txt', {
                'user': user,
                'password_reset_url': password_reset_url,
            })
            # Send the email
            send_mail(email_subject, email_body, user.email, [user.email])
            messages.success(request,"password reset link send sucessfully")
            return redirect('login')
        
    return render(request, 'user/resetpassword.html')
def password_reset_confirm(request, uidb64, token):
    
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = user_registration.objects.get(pk=uid)

    if user and default_token_generator.check_token(user, token):
        # Password reset token is valid, allow the user to reset their password
        if request.method == "POST":
            password = request.POST['password']
            print(password)
            user.password=make_password(password)
            user.save()
            messages.success(request,"password changed sucessfully")
            return redirect('login')
        return render(request, 'user/password_resetconfirm.html')
    else:
        return HttpResponse('Invalid password reset link.')
    

def change_password(request):
    try:
        if request.method == "POST":
            password1 = request.POST['password']
            password2 = request.POST['cpassword']

            if password1 != password2 :
                messages.error(request,"password dosent match")
                return render(request, 'user/change_password.html')
            if request.user:
                request.user.password=make_password(password2)
                print(request.user.password,">>>>>>>>>>>>>>>>>")
                request.user.save()
                return redirect("inventory")
        
        else:
            return render(request, 'user/change_password.html')
    except:
        return redirect("500page")
                