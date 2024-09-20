from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
        
class RigisterFormCustom(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    # email = forms.EmailField(required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords do not match.")
        
        return cleaned_data

    def save(self):
        username = self.cleaned_data['username']
        # email = self.cleaned_data['email']
        password = self.cleaned_data['password1']
        user = User.objects.create_user(username=username, password=password)
        return user
    

from .models import Department, Position, Status, Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'address', 'manager', 'status', 'position', 'department', 'image']
        widgets = {
            'position': forms.Select(attrs={'required': 'false'}),
            'department': forms.Select(attrs={'required': 'false'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['position'].help_text = "Optional: Select a position if applicable."
        self.fields['department'].help_text = "Optional: Select a department if applicable."


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'manager']
    
    def __init__(self, *args, **kwargs):
        super(DepartmentForm, self).__init__(*args, **kwargs)
        # Filter the queryset to only include employees who are managers
        self.fields['manager'].queryset = Employee.objects.filter(manager=True)
        # Allow the manager field to be empty (None)
        self.fields['manager'].required = False  # Make the manager field optional
        self.fields['manager'].empty_label = "No Manager"  # Provide a "No Manager" option

class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['name', 'salary']

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['em_status']

class EmployeeFilterForm(forms.Form):
    position = forms.ModelChoiceField(queryset=Position.objects.all(), required=False)
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False)
    status = forms.ModelChoiceField(queryset=Status.objects.all(), required=False)
    search = forms.CharField(required=False, label='Search by Name')
