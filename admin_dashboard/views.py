from user_app.forms import LoginForm, SignupForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.generic import DeleteView, UpdateView


# home page view
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_home(request):
    users = User.objects.all().order_by("username")
    data = "username"
    if request.method == "POST":
        data = request.POST["data"]
        users = User.objects.filter(username__icontains=data)
    return render(request, "custom_admin/index.html", {"users": users, "data": data})


@user_passes_test(lambda user: user.is_superuser, login_url="admin_login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_user_model(request):
    users = User.objects.all().order_by("date_joined")
    return render(request, "custom_admin/user_model.html", {"users": users})


# Admin Login View
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect("admin_home")
        else:
            return redirect("user_index")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_superuser:
                    login(request, user)
                    return redirect("admin_home")
                else:
                    context = {"form": form, "message": "User is not an Admin"}
                    return render(request, "custom_admin/login.html", context)
            else:
                context = {"form": form, "message": "Invalid Credentials"}
                return render(request, "custom_admin/login.html", context)
    else:
        form = LoginForm()
    return render(request, "custom_admin/login.html", {"form": form})


# User Details view
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_details(request, user_id):
    user = User.objects.get(pk=user_id)
    context = {
        "username": user,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "admin": user.is_superuser,
        "date": user.date_joined,
    }
    return render(request, "custom_admin/details.html", context)


# User model update view
@method_decorator(
    user_passes_test(lambda u: u.is_superuser, login_url="admin_login"), name="dispatch"
)
@method_decorator(
    cache_control(no_cache=True, must_revalidate=True, no_store=True), name="dispatch"
)
class UserModelUpdateView(UpdateView):
    model = User
    template_name = "custom_admin/update.html"
    fields = ["first_name", "last_name", "email", "username"]
    pk_url_kwarg = "user_id"

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        if User.objects.filter(email=email).exclude(pk=self.object.pk).exists():
            form.add_error(
                "email", ValidationError("This email already taken by another account")
            )
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("admin_user_details", kwargs={"user_id": self.object.pk})


# User model delete view
@method_decorator(
    user_passes_test(lambda u: u.is_superuser, login_url="admin_login"), name="dispatch"
)
@method_decorator(
    cache_control(no_cache=True, must_revalidate=True, no_store=True), name="dispatch"
)
class UserModelDeleteView(DeleteView):
    model = User
    template_name = "custom_admin/delete.html"
    success_url = reverse_lazy("admin_home")
    pk_url_kwarg = "user_id"


# ADmin user create view
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_create(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("admin_home")
    else:
        form = SignupForm()
    return render(request, "custom_admin/create.html", {"form": form})


# Admin only logout view
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
def admin_logout(request):
    logout(request)
    return redirect("admin_login")
