from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('otp/', views.otp, name='otp'),
    path('logout/', views.logout_view, name='logout'),
    path('create_user/', views.create_user, name='create_user'),
    path('users/', views.user_list, name='user_list'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete_user/<int:user_id>', views.delete_user, name='delete_user')
]