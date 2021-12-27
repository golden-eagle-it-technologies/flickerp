from crispy_forms.helper import FormHelper
from django.forms import ModelForm

from leave.models import LeaveRecord, Leave_Types


class LeaveRecordForm(ModelForm):
    class Meta:
        model = LeaveRecord
        exclude = ("employee", "leave_year")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Helper = FormHelper()

class LeaveTypeForm(ModelForm):
    class Meta:
        model = Leave_Types
        fields = '__all__'



