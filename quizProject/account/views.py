from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import CustomUser


def index(request):
    return render(request, 'base.html')


def log_in(request):
    if request.user.is_authenticated:
        return redirect('user_list')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            if CustomUser.user_exist(username):
                current_user = authenticate(username=username, password=password)
                if current_user and current_user.is_active:
                    login(request, current_user)
                    return redirect('user_list')
                else:
                    return render(request, 'log_in.html', {'wrong_password': True})
            return render(request, 'log_in.html', {'user_dont_exist': True})
        return render(request, 'log_in.html')


def register(request):
    """ used to create users and send to db"""
    if request.user.is_authenticated:
        return redirect('user_list')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            if not CustomUser.user_exist(username):
                custom_user = CustomUser.create_user(username, password)
                if custom_user:
                    return redirect(log_in)
            return render(request, 'register.html', {'user_exist': True})
        return render(request, 'register.html')


def user_list(request):
    ''' returns list of users from db'''
    return render(request, 'user_list.html',
                  {
                      'user_list': CustomUser.objects.all(),
                      'user_logged': request.user.is_authenticated
                  })


def log_out(request):
    logout(request)
    return redirect('log_in')
