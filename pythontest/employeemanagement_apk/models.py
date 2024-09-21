from django.db import models
from django.core.exceptions import ValidationError
# Database schema for the employee management system
# The schema contains four models: Status, Department, Position, and Employee.

class Department(models.Model):
    name = models.CharField(max_length=100)
    manager = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True, default=None, blank=True, related_name='managed_department')

    def save(self, *args, **kwargs):
        if self.manager is not None:
            # Ensure the manager field refers to an Employee who is a manager
            if not self.manager.manager:  # self.manager is an Employee instance
                raise ValidationError(f'The employee {self.manager.name} is not designated as a manager.')
            super(Department, self).save(*args, **kwargs)
        else:
            super(Department, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"
    
class Position(models.Model):
    #  Contains position name (Text) and salary (Number).
    name = models.TextField(max_length=100, null=False)
    salary = models.IntegerField(null=False)
    
    def __str__(self):
        return self.name

class Status(models.Model):
    # Contains the current status of the employee (e.g., in recruitmentprocess, waiting for onboarding, in probation period, normal, and resigned)
    # The status is a char field with a maximum length of 100 characters.
    em_status = models.CharField(max_length=100)
    
    def __str__(self):
        return self.em_status

class Employee(models.Model):
    # Base Requirements: Contains employee name (Text), address (Text), manager (Boolean), status (Status model), and image (Image).
    name = models.CharField(max_length=100)
    address = models.TextField(max_length=200)
    manager = models.BooleanField(default=False)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, default=None)
    image = models.ImageField(upload_to='images/')
    
    # Advacned Query: Contains department (Department model) and position (Position model).
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, default=None, blank=True)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, default=None, blank=True)
    
    def __str__(self):
        return self.name



