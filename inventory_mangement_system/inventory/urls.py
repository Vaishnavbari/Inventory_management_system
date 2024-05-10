from django.urls import path
from inventory import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("inventory/",views.inventory,name="inventory"),
    path("addinventory/",views.add_inventory_form,name="addinventory"),
    path("deleteinventory/<int:id>",views.deleteproduct,name="deleteinventory"),
    path("viewpage/<int:id>",views.viewinventory,name="view"),
    path("edit_inventory/<int:id>",views.editinventory,name="edit"),
    path("image/<int:id>",views.imagedeleted,name="image_delete"),
    path("check/<name>",views.check_product_exist,name="check"),
    path("search_product_content/",views.search_inventory_content),
    path("search_product_content/<selectedValue>",views.search_inventory_content,name="search_invertory"),
    path("search_view_content/",views.search_view_content),
    path("search_view_content/<selectedValue>",views.search_view_content,name="search_view_invertory")

   
]
if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)