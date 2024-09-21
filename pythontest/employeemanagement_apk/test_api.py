from rest_framework import status
from rest_framework.test import APITestCase
from .models import Employee, Position, Department, Status

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


