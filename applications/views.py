from django.shortcuts import render, redirect
import requests
from requests import Session
from requests_ntlm import HttpNtlmAuth
import json
from django.conf import settings as config
import datetime

# Create your views here.


def Applications(request):
    session = requests.Session()
    session.auth = config.AUTHS

    Access_Point = config.O_DATA.format("/QyApplicants")
    year = request.session['years']
    try:
        response = session.get(Access_Point, timeout=10).json()
        res = response['value']
    except requests.exceptions.ConnectionError as e:
        print(e)
    count = len(res)
    todays_date = datetime.datetime.now().strftime("%b. %d, %Y %A")
    ctx = {"today": todays_date, "year": year,
           "count": count, "res": res}
    return render(request, "app.html", ctx)


def AppDetail(request, pk):
    session = requests.Session()
    session.auth = config.AUTHS

    Access_Point = config.O_DATA.format("/QyApplicantJobApplied")
    Qualifications = config.O_DATA.format("/QyApplicantAcademicQualifications")
    Experience = config.O_DATA.format("/QyApplicantJobExperience")
    Courses = config.O_DATA.format("/QyApplicantJobProfessionalCourses")
    Memberships = config.O_DATA.format("/QyApplicantProfessionalMemberships")
    res = ''
    E_response = ''
    response = ''
    try:
        response = session.get(Access_Point, timeout=10).json()
        Qualifications_res = session.get(Qualifications, timeout=10).json()
        Experience_res = session.get(Experience, timeout=10).json()
        Courses_res = session.get(Courses, timeout=10).json()
        Memberships_res = session.get(Memberships, timeout=10).json()

        for application in response['value']:
            if application['Application_No_'] == pk:
                res = application
        for Qualifications in Qualifications_res['value']:
            if Qualifications['Applicant_No_'] == pk:
                response = Qualifications
        for course in Courses_res['value']:
            if course['Applicant_No_'] == pk:
                my_course = course
        for members in Memberships_res['value']:
            if members['Applicant_No_'] == pk:
                all_members = members
        for Experience in Experience_res['value']:
            if Experience['Applicant_No_'] == pk:
                E_response = Experience
    except requests.exceptions.ConnectionError as e:
        print(e)
    todays_date = datetime.datetime.now().strftime("%b. %d, %Y %A")
    ctx = {"today": todays_date, "res": res,
           "Qualifications": response, "experience": E_response,
           "course": my_course, "member": all_members}
    return render(request, 'appDetail.html', ctx)
