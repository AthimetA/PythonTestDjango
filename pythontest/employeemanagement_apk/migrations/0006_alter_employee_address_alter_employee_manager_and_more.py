# Generated by Django 5.1.1 on 2024-09-20 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employeemanagement_apk', '0005_alter_employee_department_alter_employee_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='address',
            field=models.TextField(max_length=200),
        ),
        migrations.AlterField(
            model_name='employee',
            name='manager',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='position',
            name='name',
            field=models.TextField(max_length=100),
        ),
    ]
