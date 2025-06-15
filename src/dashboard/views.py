from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q
import datetime
from django.core.mail import send_mail
from django.contrib import messages
from django.urls import reverse
from employee.forms import EmployeeCreateForm
from leave.models import Leave
from employee.models import *
from leave.forms import LeaveCreationForm

def dashboard(request):
    dataset = dict()
    user = request.user

    if not request.user.is_authenticated:
        return redirect('accounts:login')

    employees = Employee.objects.all()
    leaves = Leave.objects.all_pending_leaves()
    staff_leaves = Leave.objects.filter(user=user)

    dataset['employees'] = employees
    dataset['leaves'] = leaves
    dataset['staff_leaves'] = staff_leaves
    dataset['title'] = 'summary'

    return render(request, 'dashboard/dashboard_index.html', dataset)

def dashboard_employees(request):
    if not (request.user.is_authenticated and request.user.is_superuser and request.user.is_staff):
        return redirect('/')

    dataset = dict()
    departments = Department.objects.all()
    employees = Employee.objects.all()

    # pagination
    query = request.GET.get('search')
    if query:
        employees = employees.filter(
            Q(firstname__icontains=query) |
            Q(lastname__icontains=query)
        )

    paginator = Paginator(employees, 10)
    page = request.GET.get('page')
    employees_paginated = paginator.get_page(page)

    blocked_employees = Employee.objects.all_blocked_employees()
    dataset['employees'] = employees_paginated
    dataset['blocked_employees'] = blocked_employees
    dataset['departments'] = departments
    return render(request, 'dashboard/employee_app.html', dataset)

def dashboard_employees_create(request):
    if not (request.user.is_authenticated and request.user.is_superuser and request.user.is_staff):
        return redirect('/')

    if request.method == 'POST':
        form = EmployeeCreateForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            user = request.POST.get('user')
            assigned_user = User.objects.get(id=user)
            instance.user = assigned_user
            instance.title = request.POST.get('title')
            instance.image = request.FILES.get('image')
            instance.firstname = request.POST.get('firstname')
            instance.lastname = request.POST.get('lastname')
            instance.othername = request.POST.get('othername')
            instance.birthday = request.POST.get('birthday')
            role = request.POST.get('role')
            role_instance = Role.objects.get(id=role)
            instance.role = role_instance
            instance.startdate = request.POST.get('startdate')
            instance.employeetype = request.POST.get('employeetype')
            instance.employeeid = request.POST.get('employeeid')
            instance.dateissued = request.POST.get('dateissued')
            instance.save()
            return redirect('dashboard:employees')
        else:
            messages.error(request, 'Trying to create duplicate employees with a single user account', extra_tags='alert alert-warning alert-dismissible show')
            return redirect('dashboard:employeecreate')

    dataset = dict()
    form = EmployeeCreateForm()
    dataset['form'] = form
    dataset['title'] = 'register employee'
    return render(request, 'dashboard/employee_create.html', dataset)

def employee_edit_data(request, id):
    if not (request.user.is_authenticated and request.user.is_superuser and request.user.is_staff):
        return redirect('/')
    employee = get_object_or_404(Employee, id=id)
    
    if request.method == 'POST':
        form = EmployeeCreateForm(request.POST or None, request.FILES or None, instance=employee)
        if form.is_valid():
            instance = form.save(commit=False)
            assigned_user = User.objects.get(id=request.POST.get('user'))
            instance.user = assigned_user
            instance.image = request.FILES.get('image') or instance.image
            instance.firstname = request.POST.get('firstname')
            instance.lastname = request.POST.get('lastname')
            instance.othername = request.POST.get('othername')
            instance.birthday = request.POST.get('birthday')
            instance.religion = Religion.objects.get(id=request.POST.get('religion'))
            instance.nationality = Nationality.objects.get(id=request.POST.get('nationality'))
            instance.department = Department.objects.get(id=request.POST.get('department'))
            instance.hometown = request.POST.get('hometown')
            instance.region = request.POST.get('region')
            instance.residence = request.POST.get('residence')
            instance.address = request.POST.get('address')
            instance.education = request.POST.get('education')
            instance.lastwork = request.POST.get('lastwork')
            instance.position = request.POST.get('position')
            instance.ssnitnumber = request.POST.get('ssnitnumber')
            instance.tinnumber = request.POST.get('tinnumber')
            instance.role = Role.objects.get(id=request.POST.get('role'))
            instance.startdate = request.POST.get('startdate')
            instance.employeetype = request.POST.get('employeetype')
            instance.employeeid = request.POST.get('employeeid')
            instance.dateissued = request.POST.get('dateissued')
            instance.save()
            messages.success(request, 'Account Updated Successfully!', extra_tags='alert alert-success alert-dismissible show')
            return redirect('dashboard:employees')
        else:
            messages.error(request, 'Error Updating account', extra_tags='alert alert-warning alert-dismissible show')
            return HttpResponse("Form data not valid")

    dataset = dict()
    form = EmployeeCreateForm(instance=employee)
    dataset['form'] = form
    dataset['title'] = f'edit - {employee.get_full_name()}'
    return render(request, 'dashboard/employee_create.html', dataset)

def dashboard_employee_info(request, id):
    if not request.user.is_authenticated:
        return redirect('/')
    employee = get_object_or_404(Employee, id=id)
    dataset = dict()
    dataset['employee'] = employee
    dataset['title'] = f'profile - {employee.get_full_name()}'
    return render(request, 'dashboard/employee_detail.html', dataset)

# --------------------- LEAVE MANAGEMENT ----------------------------

def leave_creation(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    if request.method == 'POST':
        form = LeaveCreationForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request, 'Leave Request Sent. Wait for admin response.', extra_tags='alert alert-success alert-dismissible show')
            return redirect('dashboard:createleave')
        messages.error(request, 'Failed to submit leave request. Please check your entries.', extra_tags='alert alert-warning alert-dismissible show')
    
    dataset = {'form': LeaveCreationForm(), 'title': 'Apply for Leave'}
    return render(request, 'dashboard/create_leave.html', dataset)

def leaves_list(request):
    if not (request.user.is_staff and request.user.is_superuser):
        return redirect('/')
    return render(request, 'dashboard/leaves_recent.html', {
        'leave_list': Leave.objects.all_pending_leaves(),
        'title': 'Pending Leaves List'
    })

def leaves_approved_list(request):
    if not (request.user.is_superuser and request.user.is_staff):
        return redirect('/')
    return render(request, 'dashboard/leaves_approved.html', {
        'leave_list': Leave.objects.all_approved_leaves(),
        'title': 'Approved Leave List'
    })

def leaves_view(request, id):
    if not request.user.is_authenticated:
        return redirect('/')

    leave = get_object_or_404(Leave, id=id)
    employee = Employee.objects.filter(user=leave.user).first()
    
    if not employee:
        messages.warning(request, "No employee record found for this user. Showing basic leave details.", extra_tags='alert alert-warning alert-dismissible show')
    
    return render(request, 'dashboard/leave_detail_view.html', {
        'leave': leave,
        'employee': employee,
        'title': f'{leave.user.username}-{leave.status} leave'
    })

def approve_leave(request, id):
    if not (request.user.is_superuser and request.user.is_authenticated):
        return redirect('/')

    leave = get_object_or_404(Leave, id=id)
    employee = Employee.objects.filter(user=leave.user).first()

    if not employee:
        messages.error(request, "No employee record found for this user.", extra_tags='alert alert-warning alert-dismissible show')
        return redirect('/')

    # If approve_leave is a method, call it properly
    if hasattr(leave, 'approve_leave') and callable(leave.approve_leave):
        leave.approve_leave()
    else:
        leave.status = 'approved'
        leave.is_approved = True
        leave.save()
    print("TYPE OF employee.get_full_name:", type(employee.get_full_name))

    messages.success(request, f'Leave successfully approved for {employee.get_full_name}', extra_tags='alert alert-success alert-dismissible show')
    return redirect('dashboard:userleaveview', id=id)


def cancel_leaves_list(request):
    if not (request.user.is_superuser and request.user.is_authenticated):
        return redirect('/')
    return render(request, 'dashboard/leaves_cancel.html', {
        'leave_list_cancel': Leave.objects.all_cancel_leaves(),
        'title': 'Canceled Leave List'
    })

def unapprove_leave(request, id):
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('/')
    
    leave = get_object_or_404(Leave, id=id)
    if hasattr(leave, 'unapprove_leave') and callable(leave.unapprove_leave):
        leave.unapprove_leave()
    else:
        leave.status = 'pending'
        leave.is_approved = False
        leave.save()
    
    return redirect('dashboard:leaveslist')

def cancel_leave(request, id):
    if not (request.user.is_superuser and request.user.is_authenticated):
        return redirect('/')
    
    leave = get_object_or_404(Leave, id=id)
    if hasattr(leave, 'leaves_cancel') and callable(leave.leaves_cancel):
        leave.leaves_cancel()
    else:
        leave.status = 'canceled'
        leave.save()
    
    messages.success(request, 'Leave has been canceled', extra_tags='alert alert-success alert-dismissible show')
    return redirect('dashboard:canceleaveslist')

def uncancel_leave(request, id):
    if not (request.user.is_superuser and request.user.is_authenticated):
        return redirect('/')
    
    leave = get_object_or_404(Leave, id=id)
    leave.status = 'pending'
    leave.is_approved = False
    leave.save()
    messages.success(request, 'Leave restored to pending list', extra_tags='alert alert-success alert-dismissible show')
    return redirect('dashboard:canceleaveslist')

def leave_rejected_list(request):
    return render(request, 'dashboard/rejected_leaves_list.html', {
        'leave_list_rejected': Leave.objects.all_rejected_leaves(),
        'title': 'Rejected Leave List'
    })

def reject_leave(request, id):
    leave = get_object_or_404(Leave, id=id)
    if hasattr(leave, 'reject_leave') and callable(leave.reject_leave):
        leave.reject_leave()
    else:
        leave.status = 'rejected'
        leave.save()
    
    messages.success(request, 'Leave has been rejected', extra_tags='alert alert-success alert-dismissible show')
    return redirect('dashboard:leavesrejected')

def unreject_leave(request, id):
    leave = get_object_or_404(Leave, id=id)
    leave.status = 'pending'
    leave.is_approved = False
    leave.save()
    messages.success(request, 'Leave restored to pending list', extra_tags='alert alert-success alert-dismissible show')
    return redirect('dashboard:leavesrejected')

def view_my_leave_table(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    return render(request, 'dashboard/staff_leaves_table.html', {
        'leave_list': Leave.objects.filter(user=request.user),
        'employee': Employee.objects.filter(user=request.user).first(),
        'title': 'My Leave History'
    })
