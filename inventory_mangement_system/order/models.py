from django.db import models
from user.models import user_registration
from inventory.models import product

# Create your models here.
# order details
class order(models.Model):
    customer_name=models.ForeignKey(user_registration, on_delete=models.CASCADE)
    product_name=models.ForeignKey(product,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    order_date=models.DateField( auto_now=False, auto_now_add=False)
    tracking_id=models.CharField(max_length=50)
    select_status=(
        (0,'pending'),
        (1,'completed'),
        (2,'return'),
        (3,'Damaged'),
        (4,'cancel'),
    )
    status=models.CharField(max_length=50 ,choices=select_status,default=0)
    order_total=models.FloatField(max_length=50)
    
    def __str__(self):
        return self.customer_name
    
    def get_status_display(self):
        status_dict = dict(self.select_status)
        print(status_dict)
        return status_dict[int(self.status)]
