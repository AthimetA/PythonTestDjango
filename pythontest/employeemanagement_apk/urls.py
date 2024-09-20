from django.urls import path
from employeemanagement_apk import views

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from employeemanagement_apk.views import EmployeeViewSet, PositionViewSet, DepartmentViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'positions', PositionViewSet)
router.register(r'departments', DepartmentViewSet)

urlpatterns = [
    # Default URLs
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('database', views.database, name='database'),
    
    # Login and Registeration URLs
    path('login', views.loginPage, name='login'),
    path('register', views.registerPage, name='register'),
    path('logout', views.logoutUser, name='logout'),
    
    # Model URLs
    # Employee URLs
    path('create/employee/', views.create_employee, name='create_employee'),
    path('update/employee/<int:employee_id>', views.update_employee, name='update_employee'),
    path('delete/employee/<int:employee_id>', views.delete_employee, name='delete_employee'),
    # Position URLs
    path('create/position/', views.create_position, name='create_position'),
    path('update/position/<int:position_id>', views.update_position, name='update_position'),
    path('delete/position/<int:position_id>', views.delete_position, name='delete_position'),
    # Department URLs
    path('create/department/', views.create_department, name='create_department'),
    path('update/department/<int:department_id>', views.update_department, name='update_department'),
    path('delete/department/<int:department_id>', views.delete_department, name='delete_department'),
    # Status URLs
    path('create/status/', views.create_status, name='create_status'),
    path('update/status/<int:status_id>', views.update_status, name='update_status'),
    path('delete/status/<int:status_id>', views.delete_status, name='delete_status'),
    
    # Employee Query URLs
    path('employee_query', views.employee_query, name='employee_query'),
    
    # REST API URLs
    path('api/', include(router.urls)),
]

from django.conf import settings
from django.conf.urls.static import static

# Add Media URL for development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)