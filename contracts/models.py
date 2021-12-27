from django.db import models

# Create your models here.
from employees.models import Employee
from organisation_details.models import Position


class Contract(models.Model):
    reference_number = models.IntegerField(unique=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    type = models.CharField(max_length=40)
    effective_date = models.DateField()
    expiry_date = models.DateField()
    status = models.CharField(max_length=10, default="Active")
    risk = models.CharField(max_length=10)
    document = models.FileField(upload_to="contracts")

    def __str__(self):
        return "Contract {}".format(str(self.reference_number))

    def gross(self):
        return self.total_allowance

    def net(self):
        return (self.total_allowance-self.total_deduction)

    @property
    def total_allowance(self):
        componants = self.componants.filter(code="ALL")
        total_allowance = 0
        for componant in componants:
            if componant.method == 'fixed':
                total_allowance = total_allowance + eval(componant.amount)
            else:
                total_allowance+=0
        return total_allowance

    @property
    def total_deduction(self):
        componants = self.componants.filter(code="DED")
        total_deduction = 0
        for componant in componants:
            if componant.method == 'fixed':
                total_deduction = total_deduction + eval(componant.amount)

            if componant.method == 'formula':
                #total_deduction = total_deduction + eval(componant.amount)
                #need to implment 
                total_deduction=0

            if componant.method == 'percentage':
                total_deduction = total_deduction + \
                    (self.total * eval(componant.amount)) / 100.0
        return total_deduction


class ContractLine(models.Model):
    COMPONANT_LINE_TYPE = [
        ('BA', 'Basic Salary'),
        ('HRA', 'House rent'),
        ('DA', 'Daily Allowance'),
        ('PF', "P Tax"),
        ('ESIC', "ESIC"),
        ('GHI', "Health Cover"),
        ('TDS', 'TDS'),
        ('BO', 'Bonus'),
        ('INC', 'Incentive'),
        ('other', 'Other'),
    ]
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name="lines")
    name = models.CharField(max_length=100)
    method = models.CharField(max_length=100, choices=[
        ('formula', 'Formula'), ('fixed', 'Fixed'), ('percentage', 'Percentage')])
    condition = models.CharField(
        "Condition when this apply", max_length=500, default="1")
    type = models.CharField(max_length=100, choices=COMPONANT_LINE_TYPE)
    code = models.CharField(max_length=100, choices=[
        ('DED', 'Deduction'), ('ALL', 'Allowance')])
    amount = models.CharField("Total amount", max_length=500)


class Penalty(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()

    def __str__(self):
        return self.name


class Offence(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    resolved = models.CharField(max_length=30, choices=(('no',"No"),('yes',"Yes")))
    penalty = models.ForeignKey(Penalty, on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.name


class Termination(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    type = models.CharField(max_length=20)
    termination_letter = models.FileField(upload_to="termination_letters", blank=True)
    clearance_form = models.FileField(upload_to="termination_forms", blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    description = models.TextField()

    def __str(self):
        return self.employee
