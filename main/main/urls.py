from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('survey/', include('survey.urls')),
    path('stats/', include('stats.urls')),
    path('offices/', include('office.urls')),
    path('', views.index, name='index'),    
    path('auth/', include('authentication.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
    path('email/', include('emails.urls')),
]
