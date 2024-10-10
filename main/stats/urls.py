from django.urls import path
from . import views

urlpatterns = [
    path('sur/<int:office_id>/', views.survey_statistics, name='survey_statistics'),
    path('export/', views.export_filtered_data, name='export_filtered_data'),
    path('list/', views.survey_list, name='survey_list'),
    path('consolidated/', views.survey_consolidated, name='survey_consolidated'),
    path('sur/edit/<int:survey_id>/', views.survey_item_edit, name='survey_item_edit'),
    path('sur/delete/<int:survey_id>/', views.survey_delete, name='survey_delete'),
]
