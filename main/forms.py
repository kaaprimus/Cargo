from .models import *
from django.forms import ModelForm, DateTimeInput, TextInput, Textarea, DateInput
from django import forms
from django.contrib.auth.models import User, AnonymousUser, Permission
import re
from django.contrib.auth.forms import PasswordResetForm,SetPasswordForm

class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите адрес электронной почты',
        'type': 'email',
        'name': 'email',
        'id': 'id_email',
        }))

class UserSetPasswordForm(SetPasswordForm):
    error_messages = {
        "password_mismatch": ("The two password fields didn’t match."),
    }
    new_password1 = forms.CharField(
        label='', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите новый пароль',
        'type': 'password',
        'name': 'password1',
        'id': 'id_pass1',
        'strip': 'False',
        })
    )

    new_password2 = forms.CharField(
        label='', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите пароль еще раз',
        'type': 'password',
        'name': 'password2',
        'id': 'id_pass2',
        })
    )

# Форма для профиля   
class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'username', 'email']
        
    last_name = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control', "id" : "last_name", "placeholder" : "Введите Имя"}))
    first_name = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control', "id" : "first_name", "placeholder" : "Введите Фамилию"}))
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control', "id" : "username", "placeholder" : "Введите Имя Пользователя"}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control', "id" : "email", "placeholder" : "Введите E-mail"}))


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['cargo', 'status', 'departureDate', 
                  'departureCity', 'departureAddress', 'destinationDate',
                  'destinationCity', 'destinationAddress', 'description', 
                  'reiting', 'company', 'isDengerouse']
        
        cargo = forms.ModelChoiceField(queryset=Cargo.objects.all(), 
                                     widget=forms.Select(attrs={"class": "form-select", 'required': True, "id" : "cargo"},
            ))
        status = forms.ChoiceField(
                                choices=StatusCargo.choices,
                                widget= forms.Select(
                                        attrs={"class" : "form-select", "id" : "status-cargo"}
                                    ),
                                required=True
                            )
        departureDate = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
        departureCity = forms.CharField(max_length=85, required=True, widget=TextInput(
            attrs={"type" : "text", "class" : "form-control", "id" : "title", "placeholder" : "departureCity", "size" : 85},
            ))
        departureAddress = forms.CharField(max_length=85, required=True, widget=TextInput(
            attrs={"type" : "text", "class" : "form-control", "id" : "title", "placeholder" : "departureAddress", "size" : 85},
            ))
        destinationDate = forms.DateTimeField(required=False, 
                               widget=DateInput(
                                   attrs={"type" : "date", "class" : "form-control", 'required': True, "id" : "departureDate"}
                                   )
                               )
        destinationCity = forms.CharField(max_length=85, required=True, widget=TextInput(
            attrs={"type" : "text", "class" : "form-control", "id" : "title", "placeholder" : "departureCity", "size" : 85},
            ))
        destinationAddress = forms.CharField(max_length=85, required=True, widget=TextInput(
            attrs={"type" : "text", "class" : "form-control", "id" : "title", "placeholder" : "departureAddress", "size" : 85},
            ))
        description = forms.Textarea(

        )
        reiting = forms.FloatField(widget=forms.widgets.NumberInput(attrs={"class": "form-control", 'required': True, 'step': 0.1, 'max': 5.0, 'min': 0.0, 'id': 'reiting'}))
        company = forms.ModelChoiceField(queryset=CarrierCompany.objects.all(), 
                                     widget=forms.Select(attrs={"class": "form-control", 'required': True, "id" : "company"},
            ))
        isDengerouse = forms.BooleanField(widget=forms.widgets.RadioSelect(attrs={"class": "form-control", 'required': True, 'default':'False'}))