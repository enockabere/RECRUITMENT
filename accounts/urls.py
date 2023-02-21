from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_request, name='login'),
    path('register', views.register_request, name='register'),
    path('logout', views.logout, name='logout'),

    path('profile', views.profile_request.as_view(), name="profile"),
    path('FnApplicantDetails', views.FnApplicantDetails.as_view(), name="FnApplicantDetails"),
    path('AcademicQualifications', views.AcademicQualifications.as_view(), name="AcademicQualifications"),
    path('Counties',views.Counties.as_view(),name='Counties'),
    path('JobExperience', views.JobExperience.as_view(), name="JobExperience"),
    path('QyApplicantJobExperience', views.QyApplicantJobExperience.as_view(), name="QyApplicantJobExperience"),
    path('FnApplicantProfessionalCourse', views.FnApplicantProfessionalCourse.as_view(),name="FnApplicantProfessionalCourse"),
    path('FnApplicantAcademicQualification', views.FnApplicantAcademicQualification.as_view(), name='FnApplicantAcademicQualification'),
    path('QyApplicantJobProfessionalCourses', views.QyApplicantJobProfessionalCourses.as_view(), name="QyApplicantJobProfessionalCourses"),
    path('FnApplicantProfessionalMembership', views.FnApplicantProfessionalMembership.as_view(),name='FnApplicantProfessionalMembership'),
    path('QyApplicantProfessionalMemberships',views.QyApplicantProfessionalMemberships.as_view(),name='QyApplicantProfessionalMemberships'),
    path('FnApplicantHobby', views.FnApplicantHobby.as_view(), name='FnApplicantHobby'),
    path('QyApplicantHobbies', views.QyApplicantHobbies.as_view(), name='QyApplicantHobbies'),
    path('FnApplicantReferee', views.FnApplicantReferee.as_view(), name='FnApplicantReferee'),
    path('QyApplicantReferees', views.QyApplicantReferees.as_view(), name='QyApplicantReferees'),
]
