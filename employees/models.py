from django.db import models

from config.models import Currency
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

# Create your models here.

def limit_user_choices():
    return Q(employee__isnull=True)


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee',limit_choices_to = limit_user_choices)
    gender = models.CharField(max_length=10, default="m", choices=(("m","Male"),("f","Female"),("o","Other")))
    start_date = models.DateField()
    marital_status = models.CharField(max_length=10, default="s", choices=(("s","Single"),("m","Mariged"),("o","Other")))
    dob = models.DateField()
    mobile = models.CharField(max_length=20)
    address = models.CharField(max_length=20)
    aadhar = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default="active", choices=(("active","Active"),("notish","In Notish"),("deactive","Old employee")))
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, blank=True, default=1)
    tea_allowance = models.IntegerField(default=0)

    #Permisions
    is_recruter = models.BooleanField(default=False)
    is_hod = models.BooleanField(default=False)
    is_hr = models.BooleanField(default=False)
    is_cfo = models.BooleanField(default=False)
    is_cto = models.BooleanField(default=False)
    is_ceo = models.BooleanField(default=False)
    is_supervisor = models.BooleanField(default=False)

    @property
    def department(self):
        return self.organisationdetail.department.name

    @property
    def position(self):
        return self.organisationdetail.position.name

    @property
    def team(self):
        return self.organisationdetail.team.name

    @property
    def initial_gross_salary(self) -> int:
        return self.basic_salary + self.lunch_allowance

    @property
    def overtime_hourly_rate(self) -> float:
        """In policy they consider Gross salary in hourly rate.
        In practice, they consider basic salary"""
        hourly_rate = (float(self.basic_salary) / 26.0) / 8
        return hourly_rate

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Contacts(models.Model):
    contact_type = models.CharField(max_length=10, default="number")
    contact = models.CharField(max_length=15, null=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)


class HomeAddress(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, primary_key=True)
    district = models.CharField(max_length=20)
    division = models.CharField(max_length=20, blank=True, null=True)
    county = models.CharField(max_length=20)
    village = models.CharField(max_length=20,blank=True, null=True)
    address = models.CharField(max_length=20)
    telephone = models.CharField(max_length=20)

    def __str__(self):
        return self.district


class Certification(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    institution = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    year_completed = models.CharField(max_length=4)
    grade = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class EmergencyContact(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    relationship = models.CharField(max_length=40)
    mobile_number = models.CharField(max_length=50)
    email = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Beneficiary(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    relationship = models.CharField(max_length=40)
    mobile_number = models.CharField(max_length=40)
    percentage = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Spouse(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    gov_id_card = models.CharField(max_length=40)
    dob = models.DateField()
    occupation = models.CharField(max_length=40)
    telephone = models.CharField(max_length=40)
    nationality = models.CharField(max_length=40,blank=True, null=True)
    passport_number = models.CharField(max_length=40,blank=True, null=True)
    alien_certificate_number = models.CharField(max_length=40,blank=True, null=True)
    immigration_file_number = models.CharField(max_length=40,blank=True, null=True)

    def __str__(self):
        return self.name


class Dependant(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    dob = models.DateField()
    gender = models.CharField(max_length=40, default="")

    def __str__(self):
        return self.name



# class Deduction(models.Model):
#     employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="deductions")
#     start = models.DateField(null=True, blank=True)
#     end = models.DateField(null=True, blank=True)
#     name = models.CharField(max_length=40,default="ptax", choices=(('ptax', "PTAX"),('ghi', "GHI")))
#     amount = models.IntegerField(default=0)

#     def __str__(self):
#         return self.employee.first_name + " Deduction"



# class StatutoryDeduction(models.Model):
#     employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     amont = models.FloatField(default=0.0)
#     start = models.DateField(null=True, blank=True)
#     end = models.DateField(null=True, blank=True)

#     def __str__(self):
#         return f"Local service tax {self.local_service_tax}"



class BankDetail(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    bank_full_name = models.CharField(max_length=100,null=True, blank=True)
    name_of_bank = models.CharField(max_length=20,null=True, blank=True)
    bank_account = models.CharField(max_length=20,null=True, blank=True)
    ifsc_code = models.CharField(max_length=20,null=True, blank=True)

    def __str__(self):
        return "{} {}".format(self.name_of_bank, self.bank_account)



# class Allowance(models.Model):
#     employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="allowances")
#     date = models.DateField(null=True, blank=True)
#     end_date = models.DateField(null=True, blank=True)
#     name = models.CharField(max_length=100,null=True, blank=True)
#     amount = models.IntegerField(default=0)
#     def __str__(self):
#         return f'{self.employee.user.first_name} Saalry {name}' 


class Manager(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="managers",null=True, blank=True)
    supervisor = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="managers_supervisor",null=True, blank=True)
    lead_type = models.CharField(max_length=5, default="tl", choices = (('tl', "Team Lead"),("pm", "Project Manager")))