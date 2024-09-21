from django.test import TestCase
from .models import Employee, Department, Position, Status
import numpy as np
import random
from django.db import IntegrityError # IntegrityError is raised when a model's required field is not provided
from django.core.exceptions import ValidationError # ValidationError is raised when a model's field does not meet the requirements specified in the model definition

from django.core.files.uploadedfile import SimpleUploadedFile
from pathlib import Path
import os
from django.conf import settings
from django.db import transaction

BASE_DIR = Path(__file__).resolve().parent.parent

TEST_IMAGE_PATH = os.path.join(BASE_DIR, 'test_img\\img1.png')

LIST_STATUS = ['Active', 'Inactive', 'On Leave', 'Resigned', 'Retired']
LIST_DEPARTMENT = ['Engineering', 'HR', 'Finance', 'Marketing', 'Operations']
LIST_POSITION = ['Manager', 'Developer', 'Designer', 'Analyst', 'Tester']

# Load the test image from a file outside the APK
with open(TEST_IMAGE_PATH, 'rb') as img_file:
    GOBAL_IMAGE = SimpleUploadedFile('test_image_model.png', img_file.read(), content_type='image/png')

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
                                                            image=GOBAL_IMAGE)
            
            not_manager = get_random_employee_data()
            self.not_manager_employee = Employee.objects.create(name=not_manager['name'],
                                                                address=not_manager['address'],
                                                                manager=False,
                                                                status=not_manager['status'],
                                                                department=not_manager['department'],
                                                                position=not_manager['position'],
                                                                image=GOBAL_IMAGE)
    
        def tearDown(self):
            '''
            Clean up any uploaded files after each test.
            '''
            employees = Employee.objects.all()
            for employee in employees:
                if employee.image:
                    image_path = os.path.join(settings.MEDIA_ROOT, employee.image.name)
                    if os.path.exists(image_path):
                        os.remove(image_path)

        def test_create_department(self):
            '''
            Normal test case for creating a Department object.
            '''
            name = random.choice(self.department_names)  # Get a random department name
            department = Department.objects.create(name=name, manager=self.manager_employee)
            
            self.assertEqual(department.name, name)
            self.assertEqual(department.manager, self.manager_employee)

        def test_create_department_with_not_manager(self):
            '''
            Test case for creating a Department object with a manager who is not a manager.
            '''
            name = random.choice(self.department_names)
            with self.assertRaises(ValidationError):
                try:
                    Department.objects.create(name=name, manager=self.not_manager_employee)
                finally:
                    # Cleanup the image even if the test raises an exception
                    if self.not_manager_employee.image:
                        image_path = os.path.join(settings.MEDIA_ROOT, 'images', self.not_manager_employee.image.name)
                        if os.path.exists(image_path):
                            os.remove(image_path)

        def test_create_department_without_name(self):
            '''
            Test case for creating a Department object without a name.
            '''
            with self.assertRaises(ValidationError):
                department = Department(name=None, manager=self.manager_employee)
                department.full_clean()  # Run model validation
        
        def test_create_department_without_manager(self):
            '''
            Test case for creating a Department object without a manager.
            '''
            name = random.choice(self.department_names)
            department = Department.objects.create(name=name, manager=None)
            self.assertEqual(department.manager, None)
        
class EmployeeModelTests(TestCase):
    
    '''
    Test for the Employee model.
    '''
    
    def setUp(self):
        # This method will be run before each test
        self.statuses = LIST_STATUS
        self.departments = LIST_DEPARTMENT
        self.positions = LIST_POSITION
        
        # Prepare the data for the related models
        self.name = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=random.randint(5, 10)))
        self.address = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=random.randint(10, 30)))
        self.manager = random.choice([True, False])
        
        # Create the related models
        self.status = Status.objects.create(em_status=random.choice(self.statuses))
        manager_of_department = get_random_employee_data()
        self.manager_of_department = Employee.objects.create(name=manager_of_department['name'],
                                               address=manager_of_department['address'],
                                               manager=True,
                                               status=manager_of_department['status'],
                                               department=manager_of_department['department'],
                                               position=manager_of_department['position'],
                                               image=manager_of_department['image'])
        self.department = Department.objects.create(name=random.choice(self.departments), manager=self.manager_of_department)
        self.position = Position.objects.create(name=random.choice(self.positions), salary=np.random.randint(30000, 100000))
        
        # Load the test image from a file outside the APK
        self.image = GOBAL_IMAGE
    
    def tearDown(self):
        '''
        Clean up any uploaded files after each test.
        '''
        try:
            employee = Employee.objects.last()
            if employee and employee.image:
                image_path = os.path.join(settings.MEDIA_ROOT, employee.image.name)
                if os.path.exists(image_path):
                    os.remove(image_path)
        except Exception as e:
            # Ensure the transaction does not fail
            transaction.set_rollback(True)
            
    def test_create_employee_with_all_fields(self):
        '''
        Normal test case for creating an Employee object with all fields provided.
        '''
        employee = Employee.objects.create(name=self.name, address=self.address, manager=self.manager, status=self.status, department=self.department, position=self.position, image=self.image)
        
        self.assertEqual(employee.name, self.name)
        self.assertEqual(employee.address, self.address)
        self.assertEqual(employee.manager, self.manager)
        self.assertEqual(employee.status, self.status)
        self.assertEqual(employee.department, self.department)
        self.assertEqual(employee.position, self.position)
        # Check if the image was saved as imageFieldField
        self.assertTrue(employee.image)
        
    def test_create_employee_withnecessary_fields(self):
        '''
        Test case for creating an Employee object with only the necessary fields provided.
        '''
        employee = Employee.objects.create(name=self.name,
                                           address=self.address,
                                           manager=self.manager,
                                           status=self.status,
                                           department=None,
                                           position=None,
                                           image=self.image
                                           )
        
        self.assertEqual(employee.name, self.name)
        self.assertEqual(employee.address, self.address)
        self.assertEqual(employee.manager, self.manager)
        self.assertEqual(employee.status, self.status)
        self.assertEqual(employee.department, None)
        self.assertEqual(employee.position, None)
        self.assertTrue(employee.image)
        
    def test_create_employee_without_name(self):
        '''
        Test case for creating an Employee object without a name.
        '''
        try:
            with self.assertRaises(IntegrityError):
                Employee.objects.create(
                    name=None,
                    address=self.address,
                    manager=self.manager,
                    status=self.status,
                    department=self.department,
                    position=self.position,
                    image=self.image
                )
        finally:
            # Ensure that the image file is removed even if the test fails
            if self.image:
                image_path = os.path.join(settings.MEDIA_ROOT, 'images', self.image.name)
                if os.path.exists(image_path):
                    os.remove(image_path)
            
    def test_create_employee_without_address(self):
        '''
        Test case for creating an Employee object without an address.
        '''
        try:
            with self.assertRaises(IntegrityError):
                Employee.objects.create(
                    name=self.name,
                    address=None,
                    manager=self.manager,
                    status=self.status,
                    department=self.department,
                    position=self.position,
                    image=self.image
                )
        finally:
            # Ensure that the image file is removed even if the test fails
            if self.image:
                image_path = os.path.join(settings.MEDIA_ROOT, 'images', self.image.name)
                if os.path.exists(image_path):
                    os.remove(image_path)
            
    def test_create_employee_without_status(self):
        '''
        Test case for creating an Employee object without a status.
        '''
        with self.assertRaises(ValidationError):
            employee = Employee.objects.create(name=self.name, 
                                               address=self.address, 
                                               manager=self.manager, 
                                               status=None, 
                                               department=self.department, 
                                               position=self.position, 
                                               image=self.image)
            employee.full_clean()
             
    def test_create_employee_without_image(self):
        '''
        Test case for creating an Employee object without an image.
        '''
        with self.assertRaises(ValidationError):
            employee = Employee.objects.create(name=self.name, 
                                               address=self.address, 
                                               manager=self.manager, 
                                               status=self.status, 
                                               department=self.department, 
                                               position=self.position, 
                                               image=None)
            employee.full_clean()
                