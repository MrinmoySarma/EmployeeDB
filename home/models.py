from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.

class District(models.Model):
    district_code = models.IntegerField()
    district_name = models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.district_name

class Departments(models.Model):
    department_code = models.IntegerField()
    department_name = models.CharField(max_length=250)
    def __str__(self) -> str:
        return self.department_name
    
class Office(models.Model):
    department = models.ForeignKey(Departments, on_delete=models.CASCADE) 
    office_name = models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.office_name
    

class Designation(models.Model):
    designation_code = models.IntegerField()
    desigantion_name = models.CharField(max_length=150)
    def __str__(self) -> str:
        return self.desigantion_name


class PayBand(models.Model):
    payband_code = models.IntegerField()
    payband = models.CharField(max_length=20)
    def __str__(self) -> str:
        # To show the payband on each entry in the back-end
        return self.payband

class GradePay(models.Model):
    class Meta:
        unique_together = (('payband', 'gradepay'),)
    # Above class makes payband and gradepay a composite key 
    payband = models.ForeignKey(PayBand, on_delete=models.CASCADE)
    gradepay = models.CharField(max_length=15)
    def __str__(self) -> str:
        return self.gradepay

class Hpc(models.Model):
    hpc_code = models.IntegerField()
    hpc_name = models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.hpc_name

class Lac(models.Model):
    class Meta:
        unique_together = (('hpc', 'lac_name'),)
    hpc = models.ForeignKey(Hpc, on_delete=models.CASCADE)
    lac_name = models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.lac_name

class Employee(models.Model):
    emp_code = models.CharField(max_length=50)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE)
    gradepay = models.ForeignKey(GradePay, on_delete=models.CASCADE)
    lac = models.ForeignKey(Lac, on_delete=models.CASCADE)
    emp_grade = models.CharField(max_length=8)
    emp_type = models.CharField(max_length=25)
    bank_name = models.CharField(max_length=120)
    bank_branch = models.CharField(max_length=120)
    bank_ifsc = models.CharField(max_length=15)
    bank_ac = models.IntegerField()
    def __str__(self) -> str:
        return self.first_name
    

    

    
    
    