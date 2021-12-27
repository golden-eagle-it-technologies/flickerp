def check_role(request, role, user):
    if role == 'HR' and user.employee.is_hr == 'True':
        return HttpResponseRedirect(reverse('dashboard_page'))
    elif role == 'Employee':
        return HttpResponseRedirect(reverse('employee_role_page'))
    elif role == "HOD" and user.employee.is_hod == 'True':
        return HttpResponseRedirect(reverse('hod_role_page'))
    elif role == "CFO" and user.employee.is_cfo == 'True':
        return HttpResponseRedirect(reverse('cfo_role_page'))
    elif role == "CEO" and user.employee.is_ceo == 'True':
        return HttpResponseRedirect(reverse('ceo_role_page'))
    else:
        return render(request, 'fauth/login.html', {"message": "Wrong or No role assigned."})
