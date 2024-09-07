from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.cache import cache_control

from .forms import LoginForm, SignupForm


@login_required(login_url="user_login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_index(request):
    return render(request, "user/index.html")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_login(request):
    if request.user.is_authenticated:
        return redirect("user_index")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("user_index")
            else:
                context = {"form": form, "message": "Invalid Credentials"}
                return render(request, "user/login.html", context)
    else:
        form = LoginForm()
    return render(request, "user/login.html", {"form": form})


@login_required(login_url="user_login")
def user_logout(request):
    logout(request)
    return redirect("user_login")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_signup(request):
    if request.user.is_authenticated:
        return redirect("user_index")

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User Created Successfully")
            return redirect("user_login")
    else:
        form = SignupForm()
    return render(request, "user/signup.html", {"form": form})
