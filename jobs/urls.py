from django.urls import path
from . import views

urlpatterns = [
    path('job', views.CompanyJobs, name='job'),
    path('jobDetail/<str:pk>', views.JobDetail, name='jobDetail'),
    path('FnApplicantApplyJob/<str:pk>',
         views.FnApplicantApplyJob, name='FnApplicantApplyJob'),
    path('FnWithdrawJobApplication',
         views.FnWithdrawJobApplication, name='FnWithdrawJobApplication'),
]
