from django.db import models

# product category
class category(models.Model):
    name=models.CharField(max_length=50)
    def __str__(self):
        return self.name 


# product details
class product(models.Model):
    product_name=models.CharField(max_length=50)
    product_category=models.ForeignKey(category, on_delete=models.CASCADE)
    selliing_price=models.FloatField()
    cost_price=models.FloatField()
    quantity_in_stock=models.IntegerField()
    short_description=models.CharField( max_length=50)
    detail_description=models.CharField( max_length=250)
    total_quantity=models.CharField( max_length=50)
    def __str__(self):
        return self.product_name
                                                                                                                                                                                
# image model
class image(models.Model):
    image=models.ImageField(upload_to='img/', height_field=None, width_field=None, max_length=None)
    product_id=models.ForeignKey(product , on_delete=models.CASCADE,related_name='product')
    
