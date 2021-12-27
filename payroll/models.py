from django.db import models
from employees.models import Employee

# Create your models here.
from config.models import Currency


class PayrollRecord(models.Model):
    year = models.CharField(max_length=20)
    month = models.CharField(max_length=20)
    archived = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('year', 'month',)

    def __str__(self):
        return self.month + " " + self.year


class Payslip(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, default="")
    payroll_record = models.ForeignKey(PayrollRecord, on_delete=models.CASCADE, default="")
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, default="")
    currency_rate = models.IntegerField(default=1)
    total_days=models.floatField(default=1)
    working_days=models.floatField(default=1)
    



    def __str__(self):
        return self.employee.user.first_name + " " + self.employee.user.last_name


class CSV(models.Model):
    file_name = models.FileField(upload_to='media/csvs/')
    uploaded = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=False)

    def __str__(self):
        return f"File ID: {self.id}"
