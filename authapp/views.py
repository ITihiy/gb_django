from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm, ShopUserProfileForm
from authapp.models import ShopUser
from authapp.services import send_verify_mail


def login(request):
    login_form = ShopUserLoginForm(data=request.POST)
    next_url = request.GET.get('next', '')
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST:
                return HttpResponseRedirect(request.POST['next'])
            return HttpResponseRedirect(reverse('mainapp_index'))
    return render(request, 'authapp/login.html', {'login_form': login_form, 'next': next_url})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('mainapp_index'))


def edit(request):
    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        edit_profile_form = ShopUserProfileForm(request.POST, instance=request.user.shopuserprofile)
        if edit_form.is_valid() and edit_profile_form.is_valid():
            edit_form.save()
        return HttpResponseRedirect(reverse('authapp:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)
        edit_profile_form = ShopUserProfileForm(instance=request.user.shopuserprofile)
        return render(request, 'authapp/edit.html', {'edit_form': edit_form, 'edit_profile_form': edit_profile_form})


def register(request):
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            user = register_form.save()
            send_verify_mail(user)
        return HttpResponseRedirect(reverse('authapp:login'))
    else:
        register_form = ShopUserRegisterForm()
        return render(request, 'authapp/register.html', {'register_form': register_form})


def verify(request, email, activation_key):
    user = ShopUser.objects.filter(email=email).first()
    if user:
        if user.activation_key == activation_key and user.is_activation_key_expired():
            user.is_active = True
            user.activation_key = None
            user.activation_key_expired = None
            user.save()
            auth.login(request, user)
    return render(request, 'authapp/verify.html')
