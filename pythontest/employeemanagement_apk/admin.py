from django.contrib import admin
from employeemanagement_apk.models import Employee, Department, Status, Position

# Register your models here.
admin.site.register(Employee)
admin.site.register(Department)
admin.site.register(Status)
admin.site.register(Position)
