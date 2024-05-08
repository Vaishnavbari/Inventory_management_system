from django.contrib import admin
from .models import order
# Register your models here.
# register order
@admin.register(order)
class orderadmin(admin.ModelAdmin):
    list_display=["customer_name","product_name","quantity","order_date","tracking_id", "status","order_total",]
