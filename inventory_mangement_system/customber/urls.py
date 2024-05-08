from django.urls import path
from inventory import views
from django.conf import settings
from django.conf.urls.static import static
from customber import views

urlpatterns = [
    path("customer/",views.customerview,name="customer"),
]

if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)