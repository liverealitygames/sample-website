from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'homepage/index.html')

def login(request):
    return render(request, 'homepage/login.html')

def register(request):
    return render(request, 'homepage/register.html')