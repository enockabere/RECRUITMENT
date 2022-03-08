from django.urls import path
from . import views

urlpatterns = [
    path('job', views.CompanyJobs, name='job'),
    path('jobDetail/<str:pk>', views.JobDetail, name='jobDetail'),
]
