from django.contrib import admin
from inventory.models import product,category,image

# register product model 
@admin.register(product)
class productadmin(admin.ModelAdmin):
    list_display=['id','product_name',"product_name","product_category","selliing_price","cost_price","quantity_in_stock","short_description","detail_description"]

# register category model 
@admin.register(category)
class categoryadmin(admin.ModelAdmin):
    list_display=['id','name']


# image field 
@admin.register(image)
class imageadmin(admin.ModelAdmin):
    list_display=['id','image',"product_id"]

