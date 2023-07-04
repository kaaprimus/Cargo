from django.urls import path
from main import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    #Страница авторизации
    path('accounts/login/', views.index, name="login"),
    path('doLogin/', views.doLogin, name="doLogin"),
    path('logout/', views.logout_page, name='logout_user'),

    #URL's for carriercompany
    path('carriercompany-home/', views.carriercompanypage, name="carriercompany"),
    #URL's for shippercompany
    path('shippercompany-home/', views.shippercompanypage, name="shippercompany"),
    path('shippercompany/create-order/', views.OrderCreateView.as_view(), name="createorder"),
]