# emails/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('send-email/', views.email_view, name='send_email'),
]
