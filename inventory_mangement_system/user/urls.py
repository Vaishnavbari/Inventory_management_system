from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from user import views
urlpatterns = [
     path("",views.loginpageview,name="login"),
    path("register",views.registerpageview,name="register"),
    path("loginvalidation/",views.loginvalidation,name="loginvalidation"),
    path("baseview/",views.baseview,name="baseview"),
    path("logout/",views.logoutuser,name="logout"),
    path("dashboard/",views.dashboard,name="dashboard")
]
if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)