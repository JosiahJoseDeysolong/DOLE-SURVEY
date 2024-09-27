from django.urls import path
from . import views

urlpatterns = [
    path('', views.office_list, name='office_list'),
    path('create/', views.office_create, name='office_create'),
    path('edit/<int:office_id>/', views.office_edit, name='office_edit'),
    path('offices/<int:office_id>/delete/', views.office_delete, name='office_delete'),
    path('services/<int:office_id>/', views.office_services, name='office_services'),
    path('services/<int:office_id>/create/', views.office_create_service, name='office_create_service'),
    path('services/delete/<int:service_id>/', views.delete_service, name='delete_service'),
    path('services/edit/<int:service_id>/', views.service_edit, name='service_edit'),
]
