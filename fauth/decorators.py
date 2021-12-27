from django.contrib.auth import logout, get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


from employees.models import Employee


User = get_user_model()


def ems_login_required(function):
    def wrapper(request, *args, **kw):
        user = request.user
        if user.is_authenticated:
            return function(request, *args, **kw)
        else:
            return HttpResponseRedirect(reverse('login'))

    return wrapper


def super_admin_required(function):
    def wrapper(request, *args, **kw):
        user = request.user
        if user.is_superuser:
            return function(request, *args, **kw)
        else:
            return HttpResponseRedirect(reverse('super_admin_required_page'))

    return wrapper


def employee_required(function):
    def wrapper(request, *args, **kw):
        user = request.user
        try:
            employee = user.employee
            return function(request, *args, **kw)
        except Employee.DoesNotExist:
            return render(request, "employee_required.html")

    return wrapper


def hr_required(function):
    def wrapper(request, *args, **kw):
        user = request.user
        if user.employee.is_hr or user.employee.is_cto or user.employee.is_ceo:
            return function(request, *args, **kw)
        else:
            return HttpResponseRedirect(reverse('hr_required_page'))

    return wrapper


def hod_required(function):
    def wrapper(request, *args, **kw):
        user = request.user
        if user.employee.is_hod  or user.employee.is_cto or user.employee.is_ceo:
            return function(request, *args, **kw)
        else:
            return HttpResponseRedirect(reverse('hod_required_page'))

    return wrapper


def first_login(function):
    def wrapper(request, *args, **kwargs):
        user = request.user
        # if not user.password_changed:
        #     user.password_changed = True
        #     user.save()
        #     logout(request)
        #     return render(request, "fauth/first_time_login.html")
        # else:
        return function(request, *args, **kwargs)

    return wrapper


def employees_full_auth_required(function):

    pass


def organisation_full_auth_required(function):

    pass


def leave_full_auth_required(function):

    pass


def payroll_full_auth_required(function):

    pass


def overtime_full_auth_required(function):

    pass


def holidays_full_auth_required(function):

    pass


def recruitment_full_auth_required(function):

    pass


def contracts_full_auth_required(function):

    pass


def training_full_auth_required(function):

    pass


def learning_and_development_full_auth_required(function):

    pass

#from django.utils.decorators import method_decorator
decorators_hr = [hr_required, ems_login_required]
decorators_ceo = [hr_required, ems_login_required]
decorators_cto = [hr_required, ems_login_required]
decorators_hod = [hr_required, ems_login_required]
#@method_decorator(decorators_hr, name='dispatch')