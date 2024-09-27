from django.urls import path
from . import views

urlpatterns = [
    path('sur/<int:office_id>/', views.survey_statistics, name='survey_statistics'),
    path('export/', views.export_filtered_data, name='export_filtered_data'),
    path('list/', views.survey_list, name='survey_list'),
]
