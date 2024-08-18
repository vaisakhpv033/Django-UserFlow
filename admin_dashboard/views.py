from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.cache import cache_control
from user_app.forms import LoginForm



@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_home(request):
    return render(request, 'custom_admin/index.html')


def admin_login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_home')
        else:
            return redirect('user_index')
        
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_superuser:
                    login(request, user)
                    return redirect('admin_home')
                else:
                    context = {'form': form, 'message': 'User is not an Admin'}
                    return render(request, 'custom_admin/login.html', context)
            else:
                context = {'form': form, 'message': 'Invalid Credentials'}
                return render(request, 'custom_admin/login.html', context)
    else:
        form = LoginForm()
    return render(request, 'custom_admin/login.html', {'form': form})



def admin_logout(request):
    logout(request)
    return redirect('admin_login')
