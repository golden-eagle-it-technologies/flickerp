from django.template.loader import get_template
import datetime
from django.core.mail import EmailMultiAlternatives

from holidays.selectors import get_all_holidays

from django.contrib.auth import get_user_model
import datetime

from employees.models import Employee
from organisation_details.utils import get_department_instance
from .models import LeaveApplication, LeaveRecord, Leave_Types

user = get_user_model()


from .models import LeaveApplication
from django.db.models import Sum

def get_leave_balance(employee, l_type):
    leave_balance = 0
    days_taken = LeaveApplication.objects.filter\
        (employee_id = employee, leave_type = l_type).aggregate(Sum('no_of_days'))
        
    total_days_taken = days_taken['no_of_days__sum']

    if total_days_taken is not None:
        leave_balance = l_type.leave_days - (int(total_days_taken))
    else:
        leave_balance = l_type.leave_days

    return leave_balance

def get_employee_leave(employee):
    leave_days = 0
    days_taken = LeaveApplication.objects.filter\
        (employee_id = employee, leave_type = 4).aggregate(Sum('no_of_days'))
        
    total_days_taken = days_taken['no_of_days__sum']

    if total_days_taken is None:
        leave_days = 0
    else:
        leave_days = int(total_days_taken)

    return leave_days

def leave_balance(employee):
    days_taken = get_employee_leave(employee)
    leave_balance = 21 - int(days_taken)

    return leave_balance

# Leave Type Selectors
def get_all_leave_types():
    return Leave_Types.objects.all()


def get_leave_type(leave_type_id):
    return Leave_Types.objects.get(pk=leave_type_id)


# Leave Records Selectors
def get_all_leave_records():
    return LeaveRecord.objects.all()


def get_leave_record(employee, year):
    try:
        leave_record = LeaveRecord.objects.get(employee=employee, leave_year=year)
        return leave_record
    except LeaveRecord.DoesNotExist:
        return None


# Leave Application Selectors
def get_all_leave_applications():
    return LeaveApplication.objects.all()


# def get_employee_leave_applications(employee):
#     return LeaveApplication.objects.filter(employee=employee)


def get_employee_leave_details(employee, leave_year):
    leave_applications = LeaveApplication.objects.filter(employee=employee, apply_date__year=leave_year)

    return leave_applications


def get_leave_application(leave_application_id):
    return LeaveApplication.objects.get(pk=leave_application_id)


def get_supervisor_users(applicant):
    team = applicant.team

    all_supervisor_users = user.objects.filter(employee__is_supervisor=True)
    users = []
    for supervisor_user in all_supervisor_users:
        if supervisor_user.employee.team == team:
            users.append(supervisor_user)

    return users


def get_hod_users(applicant):
    department = applicant.department
    all_hod_users = user.objects.filter(employee__is_hod=True)
    users = []
    for hod_user in all_hod_users:
        if hod_user.employee.department == department:
            users.append(hod_user)
    return users


def get_hr_users():
    all_hr_users = user.objects.filter(employee__is_hr=True)
    return all_hr_users


def get_recent_leave_plans(limit, employee):
    return LeavePlan.objects.filter(employee=employee).order_by('-id')[:limit]


def get_hod_pending_leave_plans(hod):
    pending_leave_plans = LeavePlan.objects.filter(approval_status="Pending")
    hod_department = get_department_instance(hod)
    hod_pending_applications = []
    for pending_leave_plan in pending_leave_plans:
        applicant = pending_leave_plan.employee
        applicant_department = get_department_instance(applicant)
        if applicant_department.id is hod_department.id:
            hod_pending_applications.append(pending_leave_plan)
    return hod_pending_applications


def get_leave_plan(id):
    return LeavePlan.objects.get(id=id)


def get_approved_leave_plans(hod: Employee, month: int):
    approved_leave_plans = LeavePlan.objects.filter(approval_status="Approved", start_date__month=month)
    hod_department = get_department_instance(hod)
    hod_approved_applications = []
    for approved_leave_plan in approved_leave_plans:
        applicant = approved_leave_plan.employee
        applicant_department = get_department_instance(applicant)
        if applicant_department.id is hod_department.id:
            hod_approved_applications.append(approved_leave_plan)
    return hod_approved_applications


def get_hod_approved_leave_plans(hod):
    approved_leave_plans = LeavePlan.objects.filter(approval_status="Approved")
    hod_department = get_department_instance(hod)
    hod_approved_applications = []
    for approved_leave_plan in approved_leave_plans:
        applicant = approved_leave_plan.employee
        applicant_department = get_department_instance(applicant)
        if applicant_department.id is hod_department.id:
            hod_approved_applications.append(approved_leave_plan)
    return hod_approved_applications


def get_current_year():
    return datetime.datetime.now().year


def get_all_non_expired_leave_plan_applications():
    leave_plan_applications = LeavePlan.objects.filter(expired=False, approval_status="Pending")
    return leave_plan_applications


def get_all_non_expired_leave_applications():
    leave_applications = LeaveApplication.objects.filter(expired=False, overall_status="Pending")
    return leave_applications


def send_leave_application_email(approvers, leave_application, domain=None):
    approver_emails = []
    for approver in approvers:
        approver_emails.append(approver.email)

    context = {
        'applicant_name': leave_application.employee,
        'server_url': domain
    }

    subject, from_mail, to = 'New Leave Application', None, approver_emails
    html_content = get_template('email/application_notification.html').render(context)
    msg = EmailMultiAlternatives(subject, None, from_mail, to)
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def send_leave_plan_email(approvers, leave_plan, domain=None):
    approver_emails = []
    for approver in approvers:
        approver_emails.append(approver.email)

    context = {
        'applicant_name': leave_plan.employee,
        'server_url': domain
    }

    subject, from_mail, to = 'New Leave Plan', None, approver_emails
    html_content = get_template('email/application_notification.html').render(context)
    msg = EmailMultiAlternatives(subject, None, from_mail, to)
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def send_leave_response_email(leave_application, approver, status, domain=None):
    applicant = leave_application.employee
    user = applicant.user

    context = {
        'applicant': applicant,
        'leave_application': leave_application,
        'approver': approver,
        'status': status,
        'server_url': domain
    }

    subject, from_mail, to = 'Leave Application Response', None, user.email
    html_content = get_template('email/response_notification.html').render(context)
    msg = EmailMultiAlternatives(subject, None, from_mail, [to])
    msg.attach_alternative(html_content, 'text/html')
    #msg.send()


def get_number_of_days_without_public_holidays(start_date, end_date):
    from_date = start_date
    to_date = end_date
    date_difference = to_date - from_date
    all_days_between = (date_difference.days + 1)
    # Getting all holiday objects
    holidays = get_all_holidays()
    public_days = 0
    k = 0
    while k <= all_days_between:
        time = datetime.datetime.min.time()
        front_date_datetime = datetime.datetime.combine(from_date, time)
        check_date = front_date_datetime + datetime.timedelta(days=k)
        is_holiday = holidays.filter(date=check_date.date()).exists()

        if check_date.weekday() == 6 or is_holiday:
            public_days += 1

        k = k + 1

    no_of_days = all_days_between - public_days
    return no_of_days


def expire_leave_plan_application(application, no_of_days: int) -> bool:
    if not application.expired:
        today = datetime.date.today()
        # Application expiry date
        expiry_date = application.plan_date + datetime.timedelta(days=no_of_days)
        if today == expiry_date or today > expiry_date:
            application.expired = True
            application.approval_status = "Expired"
            application.save()
            return True
        else:
            return False
    else:
        return False


def expire_leave_application(application) -> bool:
    if not application.expired:
        today = datetime.date.today()
        # Application expiry date
        expiry_date = application.start_date
        if today == expiry_date or today > expiry_date:
            application.expired = True
            application.overall_status = "Expired"
            application.save()
            return True
        else:
            return False
    else:
        return False
