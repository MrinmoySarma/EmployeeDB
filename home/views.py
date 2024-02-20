from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Departments, District, Office, Designation, GradePay, Lac, Employee


def index(request):
    # return HttpResponse('Welcome to the body of the home page.')
    deparments = Departments.objects.all()
    context = {
        'deparments' : deparments
    }
    return render(request, 'home/index.html', context)

def about(request):
    # return HttpResponse('This is the about page')
    return render(request, 'home/about.html')





def department(request, department_code = 0):
    if department_code:
        department = Departments.objects.get(department_code = department_code)
        districts = District.objects.all()
        designations = Designation.objects.all()
        offices = Office.objects.filter(department__department_code = department_code)
        grade_pay = GradePay.objects.all()
        lac = Lac.objects.all()
        context = {
                'department':department,
                'districts':districts,
                'offices':offices,
                'designations':designations,
                'gradepays':grade_pay,
                'lac':lac,
            } 
    return render(request, 'home/getdetails.html', context)


def getdata(request):
    if request.method == 'POST':
        emp_code = request.POST['code']
        first_name = request.POST['fname']
        middle_name = request.POST['mname']
        last_name = request.POST['lname']
        email = request.POST['email']
        phone = request.POST['phone']
        district = District.objects.get(pk=request.POST['district'])
        office = Office.objects.get(pk=request.POST['office'])
        designation = Designation.objects.get(pk=request.POST['designation'])
        gradepay = GradePay.objects.get(pk=request.POST['gradepay'])
        lc = Lac.objects.get(pk=request.POST['lac'])
        grade = request.POST['grade']
        emp_type = request.POST.get('type')
        bank_name = request.POST['bank_name']
        bank_branch = request.POST['bank_branch']
        bank_ifsc = request.POST['bank_ifsc']
        bank_ac = request.POST['bank_ac']    
        new_emp = Employee(emp_code = emp_code, first_name = first_name, middle_name = middle_name,
                           last_name = last_name, email = email, phone = phone, district = district,
                           office = office, designation = designation, gradepay = gradepay, lac = lc,
                           emp_grade = grade, emp_type = emp_type, bank_name = bank_name, bank_branch = bank_branch,
                           bank_ifsc = bank_ifsc, bank_ac = bank_ac)
        new_emp.save()
        return redirect('/')
    else:
        return redirect('/department')
    





def contact(request):
    # return HttpResponse('This is the contact page.')
    return render(request, 'home/contact.html')
