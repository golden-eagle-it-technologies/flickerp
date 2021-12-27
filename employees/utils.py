from employees.models import Employee
from config.models import Currency
import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from notification.models import Notification

def add_leave_record(employee, start_date):
    date_format = "%Y-%m-%d"
    begin_date = datetime.datetime.strptime(start_date, date_format)
    start_day = begin_date.day
    start_month = begin_date.month
    start_year = begin_date.year

    current_year = datetime.date.today().year

    leave_days = 21

    if start_year == current_year:
        if start_day >= 15:
            leave_days = (12 - start_month) * 1.75
        else:
            leave_days = (12 - (start_month - 1)) * 1.75

# def add_employee_contacts(request):
#     if request.method == "POST":
#         contact_type = request.POST.get('contact_type')
#         contacts = request.POST.get('contact')
#         employee_id = request.POST.get('employee_id')

#         employee = get_employee(employee_id)

#         contact = Contact(contact_type=contact_type, contact=contacts, employee=employee)

#         employee.save()


def suspend(employee):
    employee.status = "Suspended"
    employee.save()
    return employee

def redirect_user_role(request):
    user = request.user
    # If user is an employee
    if str(user.solitonuser.soliton_role) == 'Employee':
        return render(request, "role/employee.html")
    # If user is HOD
    if str(user.solitonuser.soliton_role) == 'HOD':
        return render(request, "role/ceo.html")


# Send notification
def send_notification(solitonuser, message):
    notification = Notification(user=solitonuser, message=message)
    notification.save()

from employees.models import Employee, Contacts
from config.utils import get_ugx_currency, get_usd_currency


def get_employee(employee_id):
    return Employee.objects.get(pk=employee_id)


def get_active_employees():
    return Employee.objects.filter(status='active').order_by('start_date')


def get_passive_employees():
    return Employee.objects.filter(status='Suspended')


def get_employees_paid_in_ugx():
    ugx_currency = get_ugx_currency()
    return Employee.objects.filter(status="Active", currency=ugx_currency)


def get_employees_paid_in_usd():
    usd_currency = get_usd_currency()
    return Employee.objects.filter(status="Active", currency=usd_currency)


def get_employee_contacts(employee):
    return Contacts.objects.filter(employee=employee).order_by('contact_type')


def get_contact(contact_id):
    return Contacts.objects.get(pk=contact_id)

