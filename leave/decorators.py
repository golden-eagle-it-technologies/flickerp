from django.http import HttpResponseRedirect
from django.urls import reverse

from leave.utils import get_leave_record, get_current_year
from leave.models import LeaveRecord


def leave_record_required(function):
    def wrapper(request, *args, **kw):
        employee = request.user.employee
        try:
            current_year = get_current_year()
            Leave_Record = get_leave_record(employee, current_year)

        except LeaveRecord.DoesNotExist:
            Leave_Record = None

        if Leave_Record:
            return function(request, *args, **kw)
        else:
            return HttpResponseRedirect(reverse('no_leave_record_page'))

    return wrapper
