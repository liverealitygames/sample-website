from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from profiles.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import logging

# Create your views here.
def view(request, username):
    user: User = get_object_or_404(User, username=username)
    return render(request, 'profiles/view.html', context={"profile":user.profile})

@login_required
def edit(request):
    if request.method == "POST":
        pronouns = request.POST.get("pronouns")
        if pronouns:
            request.user.profile.pronouns = pronouns
            request.user.profile.save()
            messages.success(request, "Pronouns updated successfully")
    return render(request, 'profiles/edit.html', context={"profile":request.user.profile})

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if User.objects.filter(username=username).exists():
            messages.error(request, f"Username '{username}' is already in use")
            return redirect("profiles:register")
        user = User.objects.create_user(username=username, password=password)
        # TODO: Get images, resize, etc.
        Profile.objects.create(user=user, account_status="Under Review")
        messages.success(request, "Account created successfully")
        return redirect("profiles:login")
    return render(request, "profiles/register.html")

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("homepage:index")
        else:
            logging.info("No profile was found with those credentials.")
            messages.error(request, "No profile was found with those credentials.")
    return render(request, "profiles/login.html")

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("homepage:index")