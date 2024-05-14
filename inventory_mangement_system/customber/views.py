from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from inventory.models import product
from user.models import user_registration
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect
# Create your views here.

@login_required
def customerview(request):
    try:
        user=user_registration.objects.filter(is_superuser=0).order_by('id')

        page=Paginator(user,5)
        page_number=request.GET.get('page')
        page_obj=page.get_page(page_number)
        return render(request,"customber/customer.html",{"customber":"active","product":page_obj})
    
    except Exception as e:
        return redirect("500page")
    
@login_required
def search_customer_content(request,selectedValue=None):
    try:
        all_data=user_registration.objects.filter(is_superuser=0).values()
        if selectedValue:
            all_data=all_data.filter(first_name__icontains=selectedValue)
            
        return JsonResponse({"data":list(all_data)})
        
    except Exception as e:
        return redirect("500page")


