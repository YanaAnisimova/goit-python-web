from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.db import transaction
from django.shortcuts import redirect, render
from django.urls import reverse

from user.api import create_user  # NOQA
from .forms import RegistrationForm, LoginForm
from .models import MyUser


def register_view(request):
    if request.method == 'GET':
        form = RegistrationForm()
        return render(request, 'user/register.html', {'form': form})
    form = RegistrationForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')
        user_exists = MyUser.objects.filter(username=username).exists()
        if user_exists:
            messages.add_message(request, messages.ERROR, '* Username already exists')
            return render(request, 'user/register.html', {'form': form})
        # create user
        with transaction.atomic():
            user = create_user(username, password, email)
        # redirect to login_view
        return redirect(reverse('auth:login'))
    else:
        return render(request, 'user/register.html', {'form': form})


def login_view(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'user/login.html', {'form': form})
    form = LoginForm(request.POST)
    if form.is_valid():
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            # redirect to index view
            return redirect(reverse('finance:index'))
    else:
        # messages.add_message(request, messages.ERROR, '* E-mail or password is incorrect')
        return render(request, 'user/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect(reverse('auth:login'))
