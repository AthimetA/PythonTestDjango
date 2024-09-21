from rest_framework import serializers
from employeemanagement_apk.models import Employee, Position, Department, Status

# REST API Serializer for the Employee model
class EmployeeSerializer(serializers.ModelSerializer):
    
    # Define the fields to be serialized
    image = serializers.ImageField(required=False) # Allow image to be optional in the request
    
    class Meta:
        model = Employee
        fields = ['id', 'name', 'address', 'manager', 'status', 'position', 'department', 'image']

    def create(self, validated_data):
        return Employee.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Ensure existing image is replaced with the new one if provided
        instance.name = validated_data.get('name', instance.name)
        instance.address = validated_data.get('address', instance.address)
        instance.manager = validated_data.get('manager', instance.manager)
        instance.status = validated_data.get('status', instance.status)
        instance.position = validated_data.get('position', instance.position)
        instance.department = validated_data.get('department', instance.department)
        
        # Handle the image field specifically - if no new image is provided, keep the old one
        if 'image' in validated_data:
            instance.image = validated_data.get('image', instance.image)
        
        instance.save()
        return instance
    
class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['id', 'name', 'salary']
        
    def create(self, validated_data):
        return Position.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.salary = validated_data.get('salary', instance.salary)
        instance.save()
        return instance
    
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'manager']
        
    def create(self, validated_data):
        return Department.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.manager = validated_data.get('manager', instance.manager)
        instance.save()
        return instance
    
class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'em_status']
        
    def create(self, validated_data):
        return Status.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.em_status = validated_data.get('em_status', instance.em_status)
        instance.save()
        return instance
