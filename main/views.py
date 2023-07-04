from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from main.EmailBackEnd import EmailBackEnd
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import admin
from django.contrib.auth.decorators import user_passes_test, login_required
from django.views.decorators.cache import never_cache
from django.core.cache import cache
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from main.models import *
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse, reverse_lazy
from main.forms import *

# Create your views here.

def is_shipper_company(user):
    return user.is_authenticated and user.user_type == 1

def is_carrier_company(user):
    return user.is_authenticated and user.user_type == 2

def authentication_required(view_func):
    @login_required
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # Перенаправление на страницу входа
        return view_func(request, *args, **kwargs)
    return wrapped_view

def index(request):
    return render(request, "login.html")

def doLogin(request):
    if request.method != "POST":
        return redirect('login')
    else:
        username = request.POST.get('email'),
        user = EmailBackEnd.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
        if user != None:
            login(request, user)
            user_type = user.user_type
            if user_type == 1:
                return redirect('shippercompany')
                
            elif user_type == 2:
                return redirect('carriercompany')
            elif user_type == 3:
                return redirect('admin:index')
            else:
                messages.error(request, "Неверный логин!")
                return redirect('login')
        else:
            messages.error(request, "Неверный логин или пароль!")
            return redirect('login')

   
def logout_page(request):
    logout(request)
    cache.clear()
    return redirect('login')

@never_cache     
@authentication_required
@user_passes_test(is_carrier_company, login_url='login')
def carriercompanypage(request):
    return render(request, "carriercompany/index.html")

@never_cache     
@authentication_required
@user_passes_test(is_shipper_company, login_url='login')
def shippercompanypage(request):
    return render(request, "shippercompany/index.html")


#Order CRUD operations   
class OrderView(View):
    model = Order
    form_class = OrderForm
    active_panel = "orders-panel"
    login_url = "login_page"
    success_url = reverse_lazy("orders_create")
    extra_context = {
        "is_active" : active_panel,
        "active_regions" : "active",
        "expand_regions" : "show",
        }
    
class OrderListView(LoginRequiredMixin, OrderView, ListView):
    template_name = "shippercompany/pages/order/orders_list.html"
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        if not is_shipper_company(request.user):
            return user_passes_test(lambda u: is_shipper_company(u), login_url='login')(super().dispatch)(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)

class OrderCreateView(LoginRequiredMixin, SuccessMessageMixin, OrderView, CreateView):
    template_name = 'shippercompany/pages/order/order_form.html'
    success_message = "Запись успешно Добавлена!"

    def dispatch(self, request, *args, **kwargs):
        if not is_shipper_company(request.user):
            return user_passes_test(lambda u: is_shipper_company(u), login_url='login')(super().dispatch)(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)