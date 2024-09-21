from rest_framework import status
from rest_framework.test import APITestCase
from .models import Employee, Position, Department, Status

from django.core.files.uploadedfile import SimpleUploadedFile
from pathlib import Path
import os
from django.conf import settings
from django.db import transaction

BASE_DIR = Path(__file__).resolve().parent.parent

TEST_IMAGE_PATH = os.path.join(BASE_DIR, 'test_img', 'img4.png')

# Create an image file for testing or if it exists, use it
with open(TEST_IMAGE_PATH, 'rb') as img_file:
    GOBAL_IMG = SimpleUploadedFile(name='test_image_api.png', content=img_file.read(), content_type='image/png')

class PositionAPITests(APITestCase):
    
        def setUp(self):
            # Create test data
            self.position_data = {
                'name': 'Software Engineer',
                'salary': 100000,
            }
    
        def test_create_position(self):
            response = self.client.post('/api/positions/', self.position_data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Position.objects.count(), 1)
            self.assertEqual(Position.objects.get().name, 'Software Engineer')
    
        def test_get_position(self):
            position = Position.objects.create(**self.position_data)
            response = self.client.get(f'/api/positions/{position.id}/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['name'], position.name)
    
        def test_update_position(self):
            position = Position.objects.create(**self.position_data)
            updated_data = {'name': 'Senior Software Engineer'}
            response = self.client.put(f'/api/positions/{position.id}/', updated_data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            position.refresh_from_db()
            self.assertEqual(position.name, 'Senior Software Engineer')
    
        def test_delete_position(self):
            position = Position.objects.create(**self.position_data)
            response = self.client.delete(f'/api/positions/{position.id}/')
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            self.assertEqual(Position.objects.count(), 0)
            
class DepartmentAPITests(APITestCase):
    
        def setUp(self):
            # Create test data
            self.department_data = {
                'name': 'IT',
            }
    
        def test_create_department(self):
            response = self.client.post('/api/departments/', self.department_data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Department.objects.count(), 1)
            self.assertEqual(Department.objects.get().name, 'IT')
    
        def test_get_department(self):
            department = Department.objects.create(**self.department_data)
            response = self.client.get(f'/api/departments/{department.id}/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['name'], department.name)
    
        def test_update_department(self):
            department = Department.objects.create(**self.department_data)
            updated_data = {'name': 'HR'}
            response = self.client.put(f'/api/departments/{department.id}/', updated_data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            department.refresh_from_db()
            self.assertEqual(department.name, 'HR')
    
        def test_delete_department(self):
            department = Department.objects.create(**self.department_data)
            response = self.client.delete(f'/api/departments/{department.id}/')
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            self.assertEqual(Department.objects.count(), 0)
            
class EmployeeAPITests(APITestCase):

    def setUp(self):
        # Create a Status object if it does not exist
        self.status, self.status_created = Status.objects.get_or_create(em_status='normal')
        self.position, self.position_created = Position.objects.get_or_create(name='Software Engineer', salary=1000)
        self.department, self.department_created = Department.objects.get_or_create(name='IT')
        self.image = GOBAL_IMG

        # Create Employee data including the image
        self.employee_data_id_as_int = {
            'name': 'John Doe',
            'address': '123 Main St',
            'manager': False,
            'status': self.status.id, 
            'position': self.position.id, 
            'department': self.department.id,
            'image': self.image  
        }
        
        self.employee_data_id_as_instance = {
            'name': 'John Doe',
            'address': '123 Main St',
            'manager': False,
            'status': self.status,  
            'position': self.position,  
            'department': self.department, 
            'image': self.image  
        }
        
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
        
    def test_create_employee(self):
        response = self.client.post('/api/employees/', self.employee_data_id_as_int, format='multipart')
        print('*'*50)
        print(f'Function: test_create_employee\nResponse: {response.data}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 1)
        self.assertEqual(Employee.objects.get().name, 'John Doe')

    def test_retrieve_employee(self):
        employee = Employee.objects.create(**self.employee_data_id_as_instance)
        response = self.client.get(f'/api/employees/{employee.id}/')
        print('*'*50)
        print(f'Function: test_retrieve_employee\nResponse: {response.data}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'John Doe')
        
    def test_update_employee(self):
        employee = Employee.objects.create(**self.employee_data_id_as_instance)
        updated_data = {'name': 'Jane Doe'}
        response = self.client.patch(f'/api/employees/{employee.id}/', updated_data, format='multipart')
        print('*'*50)
        print(f'Function: test_update_employee\nResponse: {response.data}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        employee.refresh_from_db()
        self.assertEqual(employee.name, 'Jane Doe')

    def test_delete_employee(self):
        employee = Employee.objects.create(**self.employee_data_id_as_instance)
        response = self.client.delete(f'/api/employees/{employee.id}/')
        employee.full_clean()
        print('*'*50)
        print(f'Function: test_delete_employee\nResponse: {response.data}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Employee.objects.count(), 0)
    

