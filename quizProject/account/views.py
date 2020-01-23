from django.contrib.auth import authenticate
from django.shortcuts import render
from django.http import HttpResponse
from .models import CustomUser

def index(request):
    someone = request.user
    return HttpResponse(someone)

# def login(request):
#     name = request.POST.get('name')
#     password = request.POST.get('password')
#     user = authenticate(name=name,password=password)

def register(request):
    # return render(request, 'register.html')
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = CustomUser.create_user(username, password)
    if user:
        return HttpResponse('user added')
    return render(request, 'register.html')
