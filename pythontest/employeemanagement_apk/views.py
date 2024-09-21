from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

# Login and Registeration
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth.decorators import login_required

from employeemanagement_apk.forms import RigisterFormCustom


# Import the models
from employeemanagement_apk.models import Employee, Status, Department, Position

# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

@login_required(login_url='index')
def database(request):
    all_employee = Employee.objects.all()
    all_status = Status.objects.all()
    all_department = Department.objects.all()
    all_position = Position.objects.all()
    return render(request, 'database.html', {'all_employee': all_employee, 'all_status': all_status, 'all_department': all_department, 'all_position': all_position})

'''

Login and Registeration Functions


'''
def loginPage(request):
    # If the user is already logged in, redirect to the home page
    if request.user.is_authenticated:
        return redirect('index')  # Redirect to your home page (or any other page)
    
    if request.method == 'POST':
        # Use Django's built-in AuthenticationForm for better validation
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            # If the form is valid, log in the user
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                auth_login(request, user)
                return redirect('index')  # Redirect to your home page
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def registerPage(request):
    if request.method == 'POST':
        form = RigisterFormCustom(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')  # redirect to the login page
    else:
        form = RigisterFormCustom()
    return render(request, 'register.html', {'form': form})

def logoutUser(request):
    auth_logout(request)
    
    # Show a message to the user
    messages.info(request, "Logged out successfully!")
    
    return redirect('login')

'''

Form Handling Functions


'''
from employeemanagement_apk.forms import DepartmentForm, PositionForm, StatusForm, EmployeeForm

def handle_form(request, form_class, instance=None, success_message='', redirect_url='database'):
    redirect_obj = None  # Initialize redirect_obj
    form = form_class(request.POST or None, request.FILES or None, instance=instance)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, success_message)
        redirect_obj = redirect(redirect_url)

    return form, redirect_obj

# Employee URLs
@login_required(login_url='index')
def create_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee created successfully.')
            return redirect('database')
    else:
        form = EmployeeForm()
        
    statuses = Status.objects.all()
    positions = Position.objects.all()
    departments = Department.objects.all()

    return render(request, 'model/employee_create.html', {
        'form': form,
        'statuses': statuses,
        'positions': positions,
        'departments': departments,
    })

@login_required(login_url='index')
def update_employee(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    form, redirect_obj = handle_form(request, EmployeeForm, instance=employee, success_message='Employee updated successfully.')
    print(f'Redirect Object: {redirect_obj}')
    if redirect_obj:
        return redirect_obj
    else:
        # Pass the necessary context variables  
        statuses = Status.objects.all()  # Fetch all statuses
        positions = Position.objects.all()  # Fetch all positions
        departments = Department.objects.all()  # Fetch all departments

        return render(request, 'model/employee_update.html', {
            'form': form,
            'statuses': statuses,
            'positions': positions,
            'departments': departments,
        })

@login_required(login_url='index')
def delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    employee.delete()
    messages.success(request, 'Employee deleted successfully.')
    return redirect('database')

# Department URLs
@login_required(login_url='index')
def create_department(request):
    form, redirect_obj = handle_form(request, DepartmentForm, success_message='Department created successfully.')
    if redirect_obj:
        return redirect_obj
    else:
        return render(request, 'model/department_create.html', {'form': form})
    
@login_required(login_url='index')
def update_department(request, department_id):
    department = get_object_or_404(Department, pk=department_id)
    form, redirect_obj = handle_form(request, DepartmentForm, instance=department, success_message='Department updated successfully.')
    if redirect_obj:
        return redirect_obj
    else:
        return render(request, 'model/department_update.html', {'form': form})
    
@login_required(login_url='index')
def delete_department(request, department_id):
    department = Department.objects.get(pk=department_id)
    department.delete()
    messages.success(request, 'Department deleted successfully.')
    return redirect('database')

# Position URLs
@login_required(login_url='index')
def create_position(request):
    form, redirect_obj = handle_form(request, PositionForm, success_message='Position created successfully.')
    if redirect_obj:
        return redirect_obj
    else:
        return render(request, 'model/position_create.html', {'form': form})
    
@login_required(login_url='index')
def update_position(request, position_id):
    position = get_object_or_404(Position, pk=position_id)
    form, redirect_obj = handle_form(request, PositionForm, instance=position, success_message='Position updated successfully.')
    if redirect_obj:
        return redirect_obj
    else:
        return render(request, 'model/position_update.html', {'form': form})

@login_required(login_url='index')
def delete_position(request, position_id):
    position = Position.objects.get(pk=position_id)
    position.delete()
    messages.success(request, 'Position deleted successfully.')
    return redirect('database')

# Status URLs
@login_required(login_url='index')
def create_status(request):
    form, redirect_obj = handle_form(request, StatusForm, success_message='Status created successfully.')
    if redirect_obj:
        return redirect_obj
    else:
        return render(request, 'model/status_create.html', {'form': form})
    
@login_required(login_url='index')
def update_status(request, status_id):
    status = get_object_or_404(Status, pk=status_id)
    form, redirect_obj = handle_form(request, StatusForm, instance=status, success_message='Status updated successfully.')
    if redirect_obj:
        return redirect_obj
    else:
        return render(request, 'model/status_update.html', {'form': form})
    
@login_required(login_url='index')
def delete_status(request, status_id):
    status = Status.objects.get(pk=status_id)
    status.delete()
    messages.success(request, 'Status deleted successfully.')
    return redirect('database')

'''

Employee Query Functions

'''
# Employee Query URLs
from .forms import EmployeeFilterForm

def employee_query(request):
    form = EmployeeFilterForm(request.GET or None)
    employees = Employee.objects.all()

    if form.is_valid():
        if form.cleaned_data['position']:
            employees = employees.filter(position=form.cleaned_data['position'])
        if form.cleaned_data['department']:
            employees = employees.filter(department=form.cleaned_data['department'])
        if form.cleaned_data['status']:
            employees = employees.filter(status=form.cleaned_data['status'])
        if form.cleaned_data['search']:
            employees = employees.filter(name__icontains=form.cleaned_data['search'])

    context = {
        'form': form,
        'employees': employees
    }
    return render(request, 'query/employee_query.html', context)

'''

REST API Functions

'''
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from employeemanagement_apk.serializers import EmployeeSerializer, PositionSerializer, DepartmentSerializer, StatusSerializer
from rest_framework.decorators import api_view
from rest_framework import status

from rest_framework.parsers import MultiPartParser, FormParser

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    parser_classes = [MultiPartParser, FormParser]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        # Validate the serializer
        if serializer.is_valid():
            serializer.save()  # Save the instance after validation
            return Response(serializer.data)  # Now this is safe to access
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        # Validate the serializer
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        # Validate the serializer
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        # Validate the serializer
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    