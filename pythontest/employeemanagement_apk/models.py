from django.db import models

# Database schema for the employee management system
# The schema contains four models: Status, Department, Position, and Employee.

class Department(models.Model):
    # Contains department name (Text) and manager (Employee model).
    name = models.CharField(max_length=100)
    # The manager field is a foreign key to the Employee model.
    manager = models.ForeignKey('Employee', on_delete=models.CASCADE, related_name='managed_department')
    
    def __str__(self):
        return self.name + ' - ' + self.manager.name

class Position(models.Model):
    #  Contains position name (Text) and salary (Number).
    name = models.TextField()
    salary = models.IntegerField()
    
    def __str__(self):
        return self.name + ' - ' + str(self.salary)

class Status(models.Model):
    # Contains the current status of the employee (e.g., in recruitmentprocess, waiting for onboarding, in probation period, normal, and resigned)
    # The status is a char field with a maximum length of 100 characters.
    em_status = models.CharField(max_length=100)
    
    def __str__(self):
        return self.em_status

class Employee(models.Model):
    # Base Requirements: Contains employee name (Text), address (Text), manager (Boolean), status (Status model), and image (Image).
    name = models.CharField(max_length=100)
    address = models.TextField()
    manager = models.BooleanField()
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, default=None)
    image = models.ImageField(upload_to='images/')
    
    # Advacned Query: Contains department (Department model) and position (Position model).
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, default=None, blank=True)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, default=None, blank=True)
    
    def __str__(self):
        return self.name + ' - ' + (self.status.em_status if self.status else 'No Status')



