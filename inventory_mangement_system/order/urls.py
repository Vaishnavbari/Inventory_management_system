from django.urls import path
from inventory import views
from django.conf import settings
from django.conf.urls.static import static
from order import views
urlpatterns = [
    
    path("order/",views.orderview,name="order"),
    path("add_order/",views.addorder,name="addorder"),
    path("customerorderpage/",views.customer_order_page,name="cusomerorder"),
    path("show_selected_product/<int:id>",views.show_selected_product,name="show_selected_product"),
    path("count/<int:id>/<int:quantity>",views.count_price,name="count_price"),
    path("<int:id>/<selected_value>",views.statuscompletedurl,name="status_complted"),
    path("validation/<int:id>/<int:quantity>",views.quantityvalidtaion,name="quantity_validation"),
     path("search_order_content/",views.search_order_content_view),
    path("search_order_content/<selectedValue>",views.search_order_content_view,name="search_order_content"),

]
if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)