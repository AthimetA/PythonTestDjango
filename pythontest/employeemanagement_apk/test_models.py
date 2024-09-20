from django.test import TestCase
from .models import Employee, Department, Position, Status
import numpy as np
import random
from django.db import IntegrityError # IntegrityError is raised when a model's required field is not provided
from django.core.exceptions import ValidationError # ValidationError is raised when a model's field does not meet the requirements specified in the model definition

LIST_STATUS = ['Active', 'Inactive', 'On Leave', 'Resigned', 'Retired']
LIST_DEPARTMENT = ['Engineering', 'HR', 'Finance', 'Marketing', 'Operations']
LIST_POSITION = ['Manager', 'Developer', 'Designer', 'Analyst', 'Tester']

# Base Functionality Test Cases
def get_random_employee_data():
    '''
    Helper function to generate random employee data for testing.
    '''
    name = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=random.randint(5, 10)))
    address = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=random.randint(10, 30)))
    manager = random.choice([True, False])
    status = Status.objects.create(em_status=random.choice(LIST_STATUS))
    department = None
    position = None
    image = None
    
    return {'name': name, 'address': address, 'manager': manager, 'status': status, 'department': department, 'position': position, 'image': image}

'''

Position and status Test Cases

Note: Since the Position and Status models do not have any ForeignKey relationships with other models, the test cases for these models are relatively simple.:


'''
class PositionModelTests(TestCase):
    
    '''
    Test for the Position model.
    '''

    def setUp(self):
        # This method will be run before each test
        self.position_names = LIST_POSITION

    def test_create_position(self):
        '''
        Normal test case for creating a Position object.
        '''
        name = random.choice(self.position_names)  # Get a random position name
        salary = np.random.randint(30000, 100000)  # Generate a random salary between 30,000 and 100,000
        position = Position.objects.create(name=name, salary=salary)
        
        self.assertEqual(position.name, name)
        self.assertEqual(position.salary, salary)

    def test_create_position_without_name(self):
        '''
        Test case for creating a Position object without a name.
        '''
        with self.assertRaises(IntegrityError):
            Position.objects.create(name=None, salary=50000)

    def test_create_position_without_salary(self):
        '''
        Test case for creating a Position object without a salary.
        '''
        name = random.choice(self.position_names)  # Get a random position name
        position = Position(name=name, salary=None)  # Create the object without saving
        with self.assertRaises(ValidationError):
            position.full_clean()  # Validate the model before saving

        
class StatusModelTests(TestCase):
    
    '''
    Test for the Status model.
    '''
    
    def setUp(self):
        # This method will be run before each test
        self.statuses = LIST_STATUS

    def test_create_status(self):
        '''
        Normal test case for creating a Status object.
        '''
        em_status = random.choice(self.statuses)  # Get a random status
        status = Status.objects.create(em_status=em_status)
        
        self.assertEqual(status.em_status, em_status)

    def test_create_status_without_name(self):
        '''
        Test case for creating a Status object without a name.
        '''
        with self.assertRaises(IntegrityError):
            Status.objects.create(em_status=None)

    def test_create_status_with_long_name(self):
        '''
        Test case for creating a Status object with a name that exceeds the maximum length.
        '''
        long_name = 'A' * 101  # Generate a string with length 101
        status = Status(em_status=long_name)
        with self.assertRaises(ValidationError):
            status.full_clean()  # Validate the model before saving
                
'''

Employee and Department Test Cases

Employee and Department models have ForeignKey relationships with other models, so the test cases for these models are more complex than the Position and Status models. The test cases for the Employee and Department models will involve creating related objects and testing the relationships between them.

'''
class DepartmentModelTests(TestCase):
        
        '''
        Test for the Department model.
        '''
        
        def setUp(self):
            # This method will be run before each test
            self.department_names = LIST_DEPARTMENT
            
            maneger = get_random_employee_data()
            self.manager_employee = Employee.objects.create(name=maneger['name'],
                                                            address=maneger['address'],
                                                            manager=True,
                                                            status=maneger['status'],
                                                            department=maneger['department'],
                                                            position=maneger['position'],
                                                            image=maneger['image'])
            
            not_manager = get_random_employee_data()
            self.not_manager_employee = Employee.objects.create(name=not_manager['name'],
                                                                address=not_manager['address'],
                                                                manager=False,
                                                                status=not_manager['status'],
                                                                department=not_manager['department'],
                                                                position=not_manager['position'],
                                                                image=not_manager['image'])
    
        def test_create_department(self):
            '''
            Normal test case for creating a Department object.
            
            '''
            name = random.choice(self.department_names)  # Get a random department name
            # Create a random manager for the department
            department = Department.objects.create(name=name, manager=self.manager_employee)
            
            self.assertEqual(department.name, name)
            self.assertEqual(department.manager, self.manager_employee)
            
        def test_create_department_with_not_manager(self):
            '''
            Test case for creating a Department object with a manager who is not a manager.
            '''
            name = random.choice(self.department_names)
            # Create a random employee who is not a manager
            with self.assertRaises(ValidationError):
                Department.objects.create(name=name, manager=self.not_manager_employee)
                
        def test_create_department_without_name(self):
            '''
            Test case for creating a Department object without a name.
            '''
            # Attempt to create a Department without a name
            with self.assertRaises(ValidationError):
                department = Department(name=None, manager=self.manager_employee)
                department.full_clean()  # Run model validation

                
        def test_create_department_without_manager(self):
            '''
            Test case for creating a Department object without a manager.
            '''
            name = random.choice(self.department_names)
            # Attempt to create a Department without a manager
            with self.assertRaises(ValidationError):
                department = Department(name=name, manager=None)
                department.full_clean()  # Run model validation