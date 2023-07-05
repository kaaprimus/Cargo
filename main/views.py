from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from main.EmailBackEnd import EmailBackEnd
from django.contrib import messages
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
from django.utils.http import urlsafe_base64_encode
from django.conf import settings
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse
from django.contrib.auth.views import PasswordChangeView
from django.db.models import Q

# Create your views here.

def is_shipper_company(user):
    return user.is_authenticated and user.user_type == 1

def is_carrier_company(user):
    return user.is_authenticated and user.user_type == 2

def authentication_required(view_func):
    @login_required
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # Ты не вошел в аккаунт мал
        return view_func(request, *args, **kwargs)
    return wrapped_view

def redirect_to_home(request):
    return redirect('login')

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

class ProfileView(View):
    model = User
    form_class = UpdateUserForm
    success_url = reverse_lazy('update_profile')
    

class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, ProfileView, UpdateView):
    login_url = "login_page"
    success_message = "Данные успешно изменены"
    template_name = 'carriercompany/pages/user/my_profile.html'
    def get_object(self, queryset=None):
        '''This method will load the object
           that will be used to load the form
           that will be edited'''
        return self.request.user
    
class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'carriercompany/pages/user/change_password.html'
    success_message = "Пароль успешно изменён"
    success_url = reverse_lazy('update_profile')


def password_reset_request(request):
    # Установить учетные данные электронной почты
    settings.EMAIL_HOST_USER='vkrsupp@gmail.com' 
    settings.EMAIL_HOST_PASSWORD='gokuwvmbmhckgnfz' 
    if request.method == "POST": # указывает на проверку, что метод запроса должен быть ПОСТ
        # Создайте экземпляр формы UserPasswordResetForm с отправленными данными
        password_reset_form = UserPasswordResetForm(request.POST) 
        if password_reset_form.is_valid():
            # Получить адрес электронной почты, введенный в форму
            data = password_reset_form.cleaned_data['email']
            print(data)
            # Проверить, есть ли связанные пользователи с введенным адресом электронной почты
            associated_users = CustomUser.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    # Подготовьте параметры электронной почты
                    subject = "Запрос на сброс данных"
                    email_template_name = "pages/user/password_reset_email.html"
                    c = {
                        "email":user.email,
                        'domain':'http://127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                        }
                    email = render_to_string(email_template_name, c)
                    
                    try:
                        # Отправьте электронное письмо для сброса пароля
                        send_mail(subject, email, 'vkrsupp@gmail.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        
                        return HttpResponse('Invalid header found.')
                    # Перенаправление на страницу сброса пароля
                    return redirect ("/accounts/password_reset/done/")
    # Создать новый экземпляр формы UserPasswordResetForm
    password_reset_form = UserPasswordResetForm()
    #Перейти на страницу сброса пароля с формой
    return render(request=request, template_name="pages/user/password_reset.html", context={"password_reset_form":password_reset_form})

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