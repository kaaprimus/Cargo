from django.urls import path
from main import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    #Страница авторизации
    path('', views.redirect_to_home, name="index"),
    path('accounts/login/', views.index, name="login"),
    path('doLogin/', views.doLogin, name="doLogin"),
    path('logout/', views.logout_page, name='logout_user'),

    # Reset password
    path("accounts/password_reset/", views.password_reset_request, name="password_reset"),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="pages/user/password_reset_done.html"), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="pages/user/password_reset_form.html"), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="pages/user/password_reset_complete.html"), name='password_reset_complete'),

    path(r'profile/update/^', views.ProfileUpdateView.as_view(), name = 'update_profile'),
    path(r'profile/update/^/change_password/', views.ChangePasswordView.as_view(), name = 'change_password'),

    #URL's for carriercompany
    path('carriercompany-home/', views.carriercompanypage, name="carriercompany"),
    #URL's for shippercompany
    path('shippercompany-home/', views.shippercompanypage, name="shippercompany"),
    path('shippercompany/create-order/', views.OrderCreateView.as_view(), name="createorder"),


]