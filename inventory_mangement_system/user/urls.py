from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from user import views
from django.contrib.auth import views as auth_views
urlpatterns = [
     path("",views.loginpageview,name="login"),
    path("register",views.registerpageview,name="register"),
    path("loginvalidation/",views.loginvalidation,name="loginvalidation"),
    path("baseview/",views.baseview,name="baseview"),
    path("logout/",views.logoutuser,name="logout"),
    path("dashboard/",views.dashboard,name="dashboard"),
    path("password_request/",views.password_reset_request,name="password_reset"),
    path("password_request_confirm/<uidb64>/<token>/",views.password_reset_confirm,name="password_reset_confirm"),
    path("change_password/",views.change_password,name="change_password"),
    #  path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
   
    # path('accounts/password/reset/', auth_views.PasswordResetView.as_view(template_name="user/resetpassword.html"), name='password_reset'),
    # path('accounts/password/reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="user/resetpassword2.html"), name='password_reset_done'),
    # path('accounts/password/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('accounts/password/reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]


if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

