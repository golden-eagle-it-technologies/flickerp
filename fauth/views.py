from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import get_user_model

from fauth.decorators import super_admin_required, ems_login_required
from .forms import UserForm

# Create your views here.

User = get_user_model()
def get_user(id) -> User:
    user = User.objects.get(pk=id)
    return user

def get_bound_user_form(user):
    return UserForm(instance=user)
    

def login_activity_response(request, **kwargs):
    data_dict = kwargs
    email = data_dict['email'][0]  # Get first array element
    password = data_dict['password'][0]  # Get first array element
    user = authenticate(username=email, password=password)

    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('dashboard_page'))
    else:
        return render(request, "accounts/login.html", {"message": "Invalid Credentials"})


def login_view(request):
    if request.POST:
        login_data = request.POST
        return login_activity_response(request, **login_data)
    else:
        return render(request, "accounts/login.html")


def login_page(request):
    return render(request, "accounts/login.html")


# The logout view logs out the user
def logout_view(request, activity_name="Logout user"):
    logout(request)
    return render(request, "accounts/login.html", {"message": "Logged Out", "info": "info"})


def super_admin_required_page(request):
    context = {
        "admin": "active",
    }

    return render(request, "accounts/super_admin_required.html", context)


def hr_required_page(request):
    return render(request, "accounts/hr_required.html", )


def hod_required_page(request):
    return render(request, "accounts/hod_required.html", )




########################### user managment ##################################







@ems_login_required
@super_admin_required
def manage_users_page(request):
    user = request.user
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.username = user.email
            user.set_password('123')
            user.save()
            return HttpResponseRedirect(reverse(manage_users_page))
        else:
            return HttpResponseRedirect(reverse(manage_users_page))
    else:
        user_form = UserForm()

        context = {
            "user": user,
            "admin": "active",
            "users": User.objects.all(),
            "user_form": user_form,
        }
        return render(request, 'accounts/manage_users.html', context)


@super_admin_required
def edit_user_page(request, id):
    user = get_user(id)
    user_form = get_bound_user_form(user)
    if request.POST:
        user_form = UserForm(request.POST, instance=user)
        user_form.save()
        return HttpResponseRedirect(reverse(manage_users_page))
    else:
        user = request.user
        context = {
            "user": user,
            "admin": "active",
            "user_form": user_form,

        }
        return render(request, 'accounts/edit_user.html', context)



@super_admin_required
def view_users_page(request):
    user = request.user
    context = {
        "user": user,
        "admin": "active",
        "users": User.objects.all(),

    }
    return render(request, 'accounts/view_users.html', context)