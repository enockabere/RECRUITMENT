from django.urls import path
from . import views

urlpatterns = [
    path('job', views.CompanyJobs, name='job'),
]
