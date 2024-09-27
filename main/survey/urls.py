# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.survey_index, name='survey_index'),
    path('form/', views.survey, name='survey'),
    path('survey/survey_success/', views.survey_success, name='survey_success'),
    path('get-services/<int:office_id>/', views.get_services, name='get_services'),

]
