from django.urls import path
from . import views

urlpatterns = [
    path('applications', views.Applications, name="applications"),
    path('AppDetail/<str:pk>', views.AppDetail, name='AppDetail'),
]
