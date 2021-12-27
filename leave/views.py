import datetime
from calendar import HTMLCalendar
from collections import namedtuple
from employees.selectors import get_employee

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import connection, IntegrityError
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator

from employees.models import Employee
from fauth.decorators import ems_login_required, hr_required, hod_required, decorators_hr
from holidays.models import Holiday
from leave.decorators import leave_record_required
from leave.utils import (
    get_leave_type,
    get_supervisor_users,
    get_hod_users,
    get_hr_users,
    get_employee_leave_details,
    get_leave_record,
    get_recent_leave_plans, get_hod_pending_leave_plans, get_leave_plan, get_approved_leave_plans, get_current_year)
from leave.utils import send_leave_application_email, send_leave_response_email, send_leave_plan_email, \
    get_number_of_days_without_public_holidays
from notification.services import create_notification
from organisation_details.decorators import organisationdetail_required
from organisation_details.models import (
    Department,
    Team)
from organisation_details.utils import get_organisationdetail
from .models import (
    Leave_Types,
    LeaveApplication,
    LeaveRecord,
    )
from leave.forms.forms import LeaveTypeForm
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView



@method_decorator(decorators_hr, name='dispatch')
class LeaveDashboard(TemplateView):
    model = LeaveApplication
    template_name = 'leave/dashboard.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        role = ""
        user = self.request.user
        supervisor_applications, hod_applications, hr_applications = [], [], []
        if user.employee.is_supervisor:
            supervisor_applications = LeaveApplication.objects.filter(supervisor_status="Pending",
                                                                    team=user.employee.organisationdetail.team)
            role = "is_supervisor"

        if user.employee.is_hod:
            hod_applications = LeaveApplication.objects.filter(hod_status="Pending",
                                                            supervisor_status="Approved",
                                                            department=user.employee.organisationdetail.department) \
                .order_by('apply_date')
            role = "is_hod"
        if user.employee.is_hr:
            hr_applications = LeaveApplication.objects \
                .filter(hr_status="Pending", supervisor_status="Approved", hod_status="Approved").order_by('apply_date')
            role = "is_hr"

        ctx = {
            "leave_dashboard_page": "active",
            "supervisor_applications": supervisor_applications,
            "hod_applications": hod_applications,
            "hr_applications": hr_applications,
            "role": role
        }
        context.update(ctx)
        return context

@method_decorator(decorators_hr, name='dispatch')
class LeaveTypeListView(ListView):
    model = Leave_Types
    paginate_by = 100  # if pagination is desired
    template_name="leave/leave_types.html"
    context_object_name = 'types'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = LeaveTypeForm()
        return context

@login_required
def add_new_type(request):
    if request.method == 'POST':
        form = LeaveTypeForm(request.POST)
        if form.is_valid():
            leave_type = form.save()
            messages.success(request, f'Successfully Added {leave_type} leave type')
        else:
            messages.error(request, f'Something Went Wrong')

        return redirect('leave_types_page')

@method_decorator(decorators_hr, name='dispatch')
class LeaveTypeEditView(SuccessMessageMixin, UpdateView):
    model = Leave_Types
    context_object_name = "leave"
    template_name= "leave/edit_leave_type.html"
    success_url = reverse_lazy('leave_types_page')
    success_message = "Leave Type Info Updated Successfully"
    fields = "__all__"


@login_required
def delete_leave_type(request, id):
    leave = Leave_Types.objects.get(pk=id)
    leave.delete()
    messages.success(request, "Leave Type Deleted")
    return redirect('leave_types_page')


# @organisationdetail_required
# @leave_record_required
# @login_required
class LeavePage(ListView):
    template_name = "leave/leave.html"
    model = LeaveApplication
    context_object_name = "apps"
    def get_queryset(self):
        return LeaveApplication.objects.filter(employee=self.request.user.employee)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            leave_record = LeaveRecord.objects.get(
                employee=self.request.user.employee,
                leave_year=datetime.date.today().year
                )
            leave_balance = leave_record.balance
        except LeaveRecord.DoesNotExist:
            leave_balance = -1

        context['role'] = "user"
        context['leave_balance'] = leave_balance
        context['leave_types'] = Leave_Types.objects.filter(
            record__employee=self.request.user.employee,
            record__leave_year=datetime.date.today().year
            )
        #import pdb;pdb.set_trace()

        return context

# def apply_leave_page(request):
#     employee = request.user.employee
#     current_year = datetime.date.today().year

#     try:
#         leave_record = LeaveRecord.objects.get(employee=employee,
#                                                leave_year=current_year)
#         leave_balance = leave_record.balance
#     except LeaveRecord.DoesNotExist:
#         leave_balance = -1

#     context = {
#         "leave_page": "active",
#         "apps": get_employee_leave_applications(employee=employee),
#         "leave_types": Leave_Types.objects.all(),
#         "leave_balance": leave_balance,
#         "gender": request.user.employee.gender,
#         "role": "user"
#     }
#     return render(request, "leave/leave.html", context)


def no_leave_record_page(request):
    context = {
        "no_leave_record_page": "active"
    }
    return render(request, 'leave/no_leave_record.html', context)


from django.views import View

class ApplyLeave(SuccessMessageMixin, View):

    def get(self, request, *args, **kwargs):
        messages.warning(request, 'You cannot Request created leave here.')
        return render(request, "leave/leave.html")

    def post(self, request, *args, **kwargs):
        user = request.user
        employee = user.employee
        organisationdetail = get_organisationdetail(user)
        current_year = get_current_year()
        leave_type = get_leave_type(request.POST["ltype"])
        # start_date = request.POST["s_date"]
        # end_date = request.POST["e_date"]
        days_applied = int(request.POST["no_days"])
        #leave_type_days = leave_type.leave_days
        ctx = {
            'employee':user.employee,
            'leave_type':leave_type,
            'start_date':request.POST["s_date"],
            'end_date':request.POST["e_date"],
            'no_of_days':days_applied,
            'balance':leave_type.balance,
            'department':organisationdetail.department,
            'team':organisationdetail.team,
        }

        if days_applied <= leave_type.balance:
            new_balance = 0
            if leave_type.leave_type == "Annual":
                #curr_balance = leave_type.balance
                new_balance = leave_type.balance - days_applied

            if new_balance >= 0:
                leave_application = LeaveApplication(**ctx)
                if user.employee.is_supervisor:
                    leave_application.supervisor=employee
                    leave_application.supervisor_status="Approved"
                    leave_application.save()
                    approvers = get_hod_users(employee)
                    # send_leave_application_email(approvers, leave_application)
                    create_notification("Leave", f"New Leave Request from {employee.user.first_name}", approvers)
                elif user.employee.is_hod:
                    #leave_application.supervisor=employee
                    leave_application.supervisor_status="Approved"
                    leave_application.hod=employee
                    leave_application.hod_status="Approved"
                    leave_application.save()
                    approvers = get_hr_users()
                    # send_leave_application_email(approvers, leave_application)
                    create_notification("Leave", f"New Leave Request from {employee.user.first_name}", approvers)
                else:
                    leave_application.save()
                    approvers = get_supervisor_users(employee)
                    # send_leave_application_email(approvers, leave_application)
                    create_notification("Leave", f"New Leave Request from {employee.user.first_name}", approvers)
                messages.success(request, 'Leave Request Sent Successfully')
                return redirect('apply_leave_page')

            else:
                messages.warning(request, f'You have insufficient {leave_type} leave Balance {curr_balance}')
                return redirect('apply_leave_page')

        else:
            messages.warning(request, f'You cannot Request({days_applied}) for more than the\
                {leave_type.leave_type} leave days ({leave_type.leave_days})')
            return render(request, "leave/leave.html")
            #return HttpResponseRedirect('/success/')

        return render(request, self.template_name, {'form': form})


@login_required
def edit_leave_application(request):
    if request.method == "POST":
        applicant = request.user.employee

        application_id = request.POST.get("application_id")

        leave_application = LeaveApplication.objects.get(pk=application_id)

        leave_application.no_of_days = request.POST.get("no_days")
        leave_application.start_date = request.POST.get("s_date")
        leave_application.end_date = request.POST.get("e_date")
        leave_application.remarks = request.POST.get("remark")
        leave_application.save()

        messages.success(request, 'Changes saved Successfully')
        return JsonResponse({'success': True, 'redirect': "apply_leave_page"})


@login_required
def delete_leave_application(request):
    if request.method == "POST":
        applicant = request.user.employee

        application_id = request.POST.get("application_id")

        leave_application = LeaveApplication.objects.get(pk=application_id)
        leave_application.delete()

        messages.success(request, 'Request Deleted')
        return JsonResponse({'success': True, 'redirect': "apply_leave_page"})


@login_required
def leave_application_details(request, id, role):
    leave_application = LeaveApplication.objects.get(id=id)

    context = {
        "leave_application": leave_application,
        "role": role
    }

    return render(request, "leave/leave_application_details.html", context)


def check_leave_requirement(request, start_date, end_date):
    date_format = "%Y-%m-d%"

    start_date = datetime.datetime.strptime(start_date, date_format)
    apply_date = datetime.datetime.strptime(datetime.date.today(), date_format)

    difference = get_number_of_days_without_public_holidays(apply_date, start_date)

    if difference < 7:
        messages.warning(request, \
                         'leave application should be made 7 days before the leave start date')

    return JsonResponse({'message': 'leave application should be made 7 days before the leave start date'})


def approve_leave(request):
    if request.method == "POST":
        user = request.user
        application_id = request.POST.get("application_id")
        leave_application = LeaveApplication.objects.get(pk=application_id)
        employee = leave_application.employee
        l_type = leave_application.leave_type
        n_days = leave_application.no_of_days
        leave_record = LeaveRecord.objects. \
            get(employee=employee, leave_year=datetime.date.today().year)
        if user.employee.is_supervisor:
            leave_application.supervisor = user.employee
            leave_application.supervisor_status = "Approved"
            leave_application.supervisor_comment = request.POST.get("comment")
            leave_application.save()
        if user.employee.is_hod:
            leave_application.hod = user.employee
            leave_application.hod_status = "Approved"
            leave_application.hod_comment = request.POST.get("comment")
            leave_application.save()
        if user.employee.is_hr:
            curr_balance = int(leave_record.balance)
            total_applied = int(leave_record.leave_applied)
            total_taken = int(leave_record.total_taken)
            if l_type.leave_type == "Annual":
                new_balance = int(curr_balance) - int(n_days)
                total_applied += 1
                total_taken += int(n_days)
            else:
                new_balance = curr_balance

            leave_application.hr = user.employee
            leave_application.hr_status = "Approved"
            leave_application.hr_comment = request.POST.get("comment")
            leave_application.balance = new_balance
            leave_application.overall_status = "Approved"
            leave_application.save()

            LeaveRecord.objects.filter(
                employee=employee,
                leave_year=datetime.date.today().year) \
                .update(
                leave_applied=total_applied,
                total_taken=total_taken
            )
        else:
            messages.warning(request, 'Leave Approval Failed')
            return JsonResponse({'success': True, 'redirect': "leave_dashboard_page"})
        messages.success(request, 'Leave Approved Successfully')
        return JsonResponse({'success': True, 'redirect': "leave_dashboard_page"})


def reject_leave(request):
    if request.method == "POST":
        user = request.user
        employee = user.employee

        application_id = request.POST.get("application_id")
        comment = request.POST.get("comment")

        leave_application = LeaveApplication.objects.get(pk=application_id)

        if user.employee.is_supervisor:
            leave_application.supervisor = employee
            leave_application.supervisor_status = "Rejected"
            leave_application.supervisor_comment = comment

            leave_application.save()

            send_leave_response_email(leave_application, "Supervisor", "Rejected")

        elif user.employee.is_hod:
            leave_application.hod = employee
            leave_application.hod_status = "Rejected"
            leave_application.hod_comment = comment

            leave_application.save()

            send_leave_response_email(leave_application, "HOD", "Rejected")

        elif user.is_hr:
            leave_application.hr = employee
            leave_application.hr_status = "Rejected"
            leave_application.hr_comment = comment

            leave_application.save()

            send_leave_response_email(leave_application, "HR", "Rejected")

        else:
            messages.warning(request, 'Activity Failed')
            return JsonResponse({'success': True, 'redirect': "leave_dashboard_page"})

        messages.success(request, 'Leave request rejected Successfully')
        return JsonResponse({'success': True, 'redirect': "leave_dashboard_page"})


@hr_required
@ems_login_required
def leave_records(request):
    if not request.user.is_authenticated:
        return render(request, "ems_auth/login.html", {"message": None})

    current_year = datetime.date.today().year
    context = {
        "leave_page": "active",
        "leave_records": LeaveRecord.objects.filter(leave_year=current_year),
        "leave_year": current_year,
        "years": generate_years(),
    }
    return render(request, "leave/leave_records.html", context)


def add_leave_records(request):
    yr = 0

    if request.method == "POST":
        yr = request.POST["leave_yr"]

        leave_records = LeaveRecord.objects.all()
        employees = Employee.objects.all()

        if not leave_records:
            for employee in employees:
                employee_name = employee.id

                leave_record = LeaveRecord(
                    employee=employee, leave_year=yr,
                    entitlement=21, residue=0, leave_applied=0, total_taken=0,
                )

                leave_record.save()
            messages.success(request, f'Leave Records Generated for the Year - {yr}')
        else:
            try:
                year_count = leave_records.filter(leave_year=yr).count()

                entitlement = 21

                if year_count == 0:
                    for employee in employees:
                        employee_name = employee.id

                        leave_balance = leave_records.get(employee=employee, leave_year=int(yr) - 1)

                        balance = leave_balance.balance

                        residue = 0
                        if balance > 5:
                            residue = 5
                        else:
                            residue = balance

                        initial_balance = entitlement + residue

                        leave_record = LeaveRecord(employee=employee, leave_year=yr, \
                                                   entitlement=entitlement, residue=residue, leave_applied=0,
                                                   total_taken=0, \
                                                   balance=initial_balance)

                        leave_record.save()
                    messages.success(request, f'Leave Records Generated for the Year - {yr}')
            except:
                messages.warning(request, f'Records Not created for the year - {yr}')
        context = {
            "leave_page": "active",
            "leave_records": LeaveRecord.objects.filter(leave_year=yr),
            "leave_year": yr,
            "years": generate_years()
        }
        return render(request, "leave/leave_records.html", context)


def generate_years():
    current_year = datetime.date.today().year

    next_years = []

    start_year = current_year - 3
    i = 0
    while i < 8:
        next_years.append(start_year + 1)
        start_year += 1
        i += 1

    return next_years


def get_end_date(request):
    if request.method == "GET":
        date_format = "%Y-%m-%d"
        start_date = request.GET["startDate"]
        days = request.GET["no_of_days"]
        if start_date and days:
            no_days = int(days)
            from_date = datetime.datetime.strptime(start_date, date_format)
            holidays = Holiday.objects.all()
            k = 0
            public_days = 0
            while k < no_days:
                check_date = from_date + datetime.timedelta(days=k)
                is_holiday = holidays.filter(date=check_date.date()).exists()
                if check_date.weekday() == 6 or is_holiday:
                    public_days += 1
                k += 1
            end_date = from_date + datetime.timedelta(days=(no_days + public_days) - 1)
            if end_date is None:
                return JsonResponse({'success': False, 'message': 'No Date returned'})

            return JsonResponse({'success': True, 'end_date': end_date.date()})
        else:
            return JsonResponse({'success': False, 'message': "Start Date and/or Number of days Not Specified"})


def get_number_of_days_between_two_dates(request):
    date_format = "%Y-%m-%d"
    start_date = datetime.datetime.strptime(request.GET["start_date"], date_format)
    end_date = datetime.datetime.strptime(request.GET["end_date"], date_format)
    number_of_days = get_number_of_days_without_public_holidays(start_date, end_date)
    return JsonResponse({'success': True, 'number_of_days': number_of_days})


def get_no_of_days(request):
    if request.method == "GET":
        employee = request.user.employee
        leave_type = request.GET['leave_type']

        if leave_type:
            leave = Leave_Types.objects.get(id=leave_type)

            if leave.leave_type != "Annual":
                no_of_days = leave.leave_days

            else:
                # leave_records = LeaveRecord.objects.get(employee=employee, \
                #                                         leave_year=datetime.date.today().year)
                no_of_days = leave.balance

            return JsonResponse({'success': True, 'no_of_days': no_of_days, 'leave': leave.leave_type})
        else:
            return JsonResponse({'success': False, 'message': 'No such Leave Type'})


# def annual_calendar(request):
#     # first_day = calendar.TextCalendar(calendar.MONDAY)
#     # annual_calendar = first_day.formatyear(2019)
#     context = {
#         "annual_calendar": "active",
#         "employees": Employee.objects.all()
#     }

#     return render(request, 'leave/annual_calendar.html', context)


# def leave_planer(request):
#     # The line requires the user to be authenticated before accessing the view responses.
#     if not request.user.is_authenticated:
#         # if the user is not authenticated it renders a login page
#         return render(request, 'registration/login.html', {"message": None})

#     current_year = datetime.datetime.now().year

#     context = {
#         "leave_planner": "active",
#         "planner": annual_planner.objects.all(),
#         "leave_types": Leave_Types.objects.all(),
#         "employees": Employee.objects.all(),
#         "year": current_year
#     }
#     return render(request, 'leave/leave_planner.html', context)


def add_new_absence(request):
    if request.method == "POST":
        employee = Employee.objects.get(pk=request.user.id)
        leave = Leave_Types.objects.get(pk=request.POST["leave_type"])
        from_date = request.POST["from_date"]
        to_date = request.POST["to_date"]

    date_format = "%Y-%m-%d"
    leave_year = datetime.datetime.strptime(from_date, date_format).year
    # leave_month = calendar.month_name[datetime.datetime.strptime(from_date, date_format).month]
    # leave_days = calculate_leave_days(from_date, to_date)

    try:
        if leave_days >= 1:
            planner = annual_planner(leave_year=leave_year, date_from=from_date, date_to=to_date, \
                                     employee=employee, leave=leave, leave_month=leave_month[0:3],
                                     no_of_days=leave_days)

            planner.save()

            messages.success(request, f'Data Saved Successfully')

            overlaps = get_leave_overlap(from_date, to_date)

            if overlaps > 1:
                messages.warning(request, f'There are {overlaps - 1} Overlap(s) during the selected period.\
                    \n Click to View Overlaps')

        else:
            messages.warning(request, f'Invalid Date Range')

        return redirect('leave_planner')

    except:
        messages.error(request, f'Data Not Saved, Check you inputs and try again!')

        #  return redirect('leave_planner')


# def get_leave_overlap(start_date, end_date):
#     absences = annual_planner.objects.all()

#     Range = namedtuple('Range', ['start', 'end'])

#     date_format = "%Y-%m-%d"
#     from_date = datetime.datetime.strptime(start_date, date_format)
#     to_date = datetime.datetime.strptime(end_date, date_format)

#     r1 = Range(start=from_date.date(), end=to_date.date())

#     overlap = 0
#     overlap_count = 0
#     for absence in absences:
#         r2 = Range(start=absence.date_from, end=absence.date_to)
#         latest_start = max(r1.start, r2.start)
#         earliest_end = min(r1.end, r2.end)
#         delta = (earliest_end - latest_start).days + 1
#         overlap = max(0, delta)

#         if overlap > 0:
#             overlap_count += 1

#     return overlap_count


# def Leave_planner_summary(request):
#     # The line requires the user to be authenticated before accessing the view responses.
#     if not request.user.is_authenticated:
#         # if the user is not authenticated it renders a login page
#         return render(request, 'registration/login.html', {"message": None})

#     department_id = 0
#     team_id = 0
#     if request.method == "POST":
#         department_id = request.POST["department"]
#         team_id = request.POST["team"]

#     # Select multiple records
#     all_plans = None
#     with connection.cursor() as cursor:
#         cursor.execute(f"SELECT e.first_name || ' ' || e.last_name as Employee,\
#         SUM(CASE WHEN leave_month = 'Jan' THEN no_of_days ELSE 0 END) as Jan,\
#         SUM(CASE WHEN leave_month = 'Feb' THEN no_of_days ELSE 0 END) as Feb,\
#         SUM(CASE WHEN leave_month = 'Mar' THEN no_of_days ELSE 0 END) as Mar,\
#         SUM(CASE WHEN leave_month = 'Apr' THEN no_of_days ELSE 0 END) as Apr,\
#         SUM(CASE WHEN leave_month = 'May' THEN no_of_days ELSE 0 END) as May,\
#         SUM(CASE WHEN leave_month = 'Jun' THEN no_of_days ELSE 0 END) as Jun,\
#         SUM(CASE WHEN leave_month = 'Jul' THEN no_of_days ELSE 0 END) as Jul,\
#         SUM(CASE WHEN leave_month = 'Aug' THEN no_of_days ELSE 0 END) as Aug,\
#         SUM(CASE WHEN leave_month = 'Sep' THEN no_of_days ELSE 0 END) as Sep,\
#         SUM(CASE WHEN leave_month = 'Oct' THEN no_of_days ELSE 0 END) as Oct,\
#         SUM(CASE WHEN leave_month = 'Nov' THEN no_of_days ELSE 0 END) as Nov,\
#         SUM(CASE WHEN leave_month = 'Dec' THEN no_of_days ELSE 0 END) as Dec\
#         FROM employees_employee e LEFT OUTER JOIN leave_annual_planner l ON e.id=l.employee_id\
# 		WHERE e.id IN \
#             (SELECT employee_id FROM employees_organisationdetail \
#                 WHERE department_id={department_id} AND team_id={team_id})\
#         GROUP BY e.id;")
#         all_plans = cursor.fetchall()
#     # DB API fetchall produces a list of tuples

#     context = {
#         "plans": all_plans,
#         "departments": Department.objects.all(),
#         "teams": Team.objects.all()
#     }
#     return render(request, 'leave/annual_calendar.html', context)


def leave_calendar(request, month=datetime.date.today().month, year=datetime.date.today().year):
    year = int(year)
    month = int(month)

    if year < 1900 or year > 2099:
        year = datetime.date.today().year

    month_name = calendar.month_name[month]

    cal = HTMLCalendar.formatmonth(year, month)

    context = {
        "title": year,
        "calendar": cal
    }
    return render(request, 'leave/leave_calendar.html', context)


# @login_required
# @organisationdetail_required
# def create_leave_plan_page(request):
#     user = request.user
#     employee = user.employee

#     if request.POST:
#         start_date = request.POST.get("start_date")
#         end_date = request.POST.get("end_date")
#         description = request.POST.get("description")

#         try:
#             new_leave_plan = LeavePlan.objects.create(
#                 employee=employee,
#                 start_date=start_date,
#                 end_date=end_date,
#                 description=description
#             )
#             receivers = get_hod_users(employee)
#             create_notification("New Leave Plan", f"A leave plan from {employee} pending approval", receivers)
#         except IntegrityError:
#             return HttpResponseRedirect(reverse(create_leave_plan_page))

#     context = {
#         "leave_plans": "",
#         "leave_page": "active",
#         "recent_leave_plans": get_recent_leave_plans(5, employee),
#     }
#     return render(request, "leave/create_leave_plan.html", context)


# @hod_required
# @login_required
# @organisationdetail_required
# def approve_leave_plan_page(request):
#     hod = request.user.employee
#     leave_plans = get_hod_pending_leave_plans(hod)
#     context = {
#         "leave_plans": leave_plans,
#         "leave_page": "active"
#     }
#     return render(request, "leave/approve_leave_plans.html", context)


# @hod_required
# @login_required
# @organisationdetail_required
# def approve_leave_plan(request, id):
#     leave_plan = get_leave_plan(id=id)
#     leave_plan.approval_status = "Approved"
#     leave_plan.save()
#     create_notification("Leave Plan Approved", f"Your leave plan has been approved", [leave_plan.employee])
#     messages.warning(request, f'Leave plan approved')
#     return HttpResponseRedirect(reverse(approve_leave_plan_page))


# @login_required
# @organisationdetail_required
# def reject_leave_plan(request, id):
#     leave_plan = get_leave_plan(id=id)
#     leave_plan.approval_status = "Rejected"
#     leave_plan.save()
#     create_notification("Leave Plan Rejected", f"Your leave plan has been rejected", [leave_plan.employee])
#     messages.warning(request, f'Leave plan rejected')
#     return HttpResponseRedirect(reverse(approve_leave_plan_page))


# @hod_required
# @login_required
# @organisationdetail_required
# def leave_plans_page(request):
#     hod = request.user.employee
#     current_month = datetime.datetime.today().month
#     approved_leave_plans = get_approved_leave_plans(hod, month=current_month)
#     context = {
#         "leave_plans": "",
#         "leave_page": "active",
#         "january": len(get_approved_leave_plans(hod, 1)),
#         "february": len(get_approved_leave_plans(hod, 2)),
#         "march": len(get_approved_leave_plans(hod, 3)),
#         "april": len(get_approved_leave_plans(hod, 4)),
#         "may": len(get_approved_leave_plans(hod, 5)),
#         "june": len(get_approved_leave_plans(hod, 6)),
#         "july": len(get_approved_leave_plans(hod, 7)),
#         "august": len(get_approved_leave_plans(hod, 8)),
#         "september": len(get_approved_leave_plans(hod, 9)),
#         "october": len(get_approved_leave_plans(hod, 10)),
#         "november": len(get_approved_leave_plans(hod, 11)),
#         "december": len(get_approved_leave_plans(hod, 12)),
#         "approved_leave_plans": approved_leave_plans,
#     }
#     return render(request, "leave/leave_plans.html", context)


# @login_required
# @organisationdetail_required
# def month_leave_plans_page(request, month_id):
#     hod = request.user.employee
#     leave_plans = get_approved_leave_plans(hod, month_id)
#     context = {
#         "leave_page": "active",
#         "leave_plans": leave_plans
#     }
#     return render(request, "leave/month_leave_plans.html", context)

@login_required
@organisationdetail_required
def employee_leave_details(request, leave_year, employee_id):
    employee = get_employee(employee_id)
    leave_applications = get_employee_leave_details(employee, leave_year)
    
    leave_record = get_leave_record(employee, leave_year)
    context = {
        "leave_page": "active",
        "employee": employee,
        "applications": leave_applications,
        "balance": leave_record.balance
    }
    return render(request, "leave/employee_leave_details.html", context)

