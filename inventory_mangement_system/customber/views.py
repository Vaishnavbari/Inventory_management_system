from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from inventory.models import product
from user.models import user_registration
from django.core.paginator import Paginator
# Create your views here.

@login_required
def customerview(request):
    user=user_registration.objects.filter(is_superuser=0).order_by('id')

    page=Paginator(user,5)
    page_number=request.GET.get('page')
    page_obj=page.get_page(page_number)
    return render(request,"customber/customer.html",{"customber":"active","product":page_obj})

