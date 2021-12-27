from django.forms import ModelForm, EmailField, TextInput

from .models import Employee, Manager

class EmployeeForm(ModelForm):
    # email = EmailField(
    #     label='',
    #     required=True,
    #     widget=TextInput(attrs={'placeholder': 'Enter Email', 'class': 'form-control'})
    # )

    class Meta:
        model = Employee
        # fields = ['email', 'is_superuser', 'is_staff', 'is_active','first_name', 'last_name']
        fields = "__all__"

class SuperviserForm(ModelForm):
    class Meta:
        model = Manager
        fields = ('supervisor', 'lead_type')
