from django.contrib import admin
from .models import user_registration

# Register your models here.

# register user model 
@admin.register(user_registration)
class usermodel(admin.ModelAdmin):
    list_display=['id','first_name',"last_name","username"]