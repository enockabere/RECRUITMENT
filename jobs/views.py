from audioop import reverse
from django.shortcuts import render, redirect
import requests
from requests import Session
from requests_ntlm import HttpNtlmAuth
import json
from django.conf import settings as config
import datetime
from datetime import date
from django.contrib import messages
# Create your views here.


def CompanyJobs(request):
    session = requests.Session()
    session.auth = config.AUTHS

    Access_Point = config.O_DATA.format("/QyRecruitmentRequests")
    submitted = config.O_DATA.format("/QyApplicantJobApplied")

    todays_date = date.today()
    year = todays_date.year
    Job = []
    Sub = []
    try:
        response = session.get(Access_Point, timeout=10).json()
        submitted_res = session.get(submitted, timeout=10).json()
        for job in response['value']:
            if job['Submitted_To_Portal'] == True:
                output_json = json.dumps(job)
                Job.append(json.loads(output_json))
        for subs in submitted_res['value']:
            if subs['Application_No_'] == request.session['No_']:
                output_json = json.dumps(subs)
                Sub.append(json.loads(output_json))
    except requests.exceptions.ConnectionError as e:
        print(e)
    count = len(Job)
    counter = len(Sub)
    todays_date = datetime.datetime.now().strftime("%b. %d, %Y %A")
    if request.session['username']:
        my_name = request.session['username']
    else:
        my_name = "John Doe"
    ctx = {"today": todays_date, "year": year,
           "count": count, "res": Job, "sub": Sub,
           "counter": counter, "my_name": my_name}
    return render(request, 'job.html', ctx)


def JobDetail(request, pk):
    session = requests.Session()
    session.auth = config.AUTHS

    Access_Point = config.O_DATA.format("/QyRecruitmentRequests")
    Qualifications = config.O_DATA.format("/QyJobAcademicQualifications")
    Experience = config.O_DATA.format("/QyJobExperienceQualifications")
    Industry = config.O_DATA.format("/QyJobIndustries")
    Memberships = config.O_DATA.format("/QyProfessionalMemberships")
    Responsibilities = config.O_DATA.format("/QyJobResponsibilities")
    Skills = config.O_DATA.format("/QyJobKnowledgeSkills")
    Courses = config.O_DATA.format("/QyProfessionalCourses")
    JobMembeships = config.O_DATA.format("/QyJobProfessionalMembeships")
    Positions = config.O_DATA.format("/QyJobPositionsSupervising")
    Attachments = config.O_DATA.format("/QyJobAttachments")
    res = ''
    E_response = ''
    try:
        response = session.get(Access_Point, timeout=10).json()
        Qualifications_res = session.get(Qualifications, timeout=10).json()
        Experience_res = session.get(Experience, timeout=10).json()
        Industry_res = session.get(Industry, timeout=10).json()
        Memberships_res = session.get(Memberships, timeout=10).json()
        Responsibilities_res = session.get(Responsibilities, timeout=10).json()
        Skills_res = session.get(Skills, timeout=10).json()
        Courses_res = session.get(Courses, timeout=10).json()
        JobMembeships_res = session.get(JobMembeships, timeout=10).json()
        Positions_res = session.get(Positions, timeout=10).json()
        Attachments_res = session.get(Attachments, timeout=10).json()

        RESPOs = []
        Skill = []
        Course = []
        Member = []
        Position = []
        Attachment = []

        All_Industry = Industry_res['value']
        All_Memberships = Memberships_res['value']
        for job in response['value']:
            if job['Job_ID'] == pk:
                res = job
        for Qualifications in Qualifications_res['value']:
            if Qualifications['Job_ID'] == pk:
                response = Qualifications
        for Experience in Experience_res['value']:
            if Experience['Job_ID'] == pk:
                E_response = Experience
        for Responsibilities in Responsibilities_res['value']:
            if Responsibilities['Code'] == pk:
                output_json = json.dumps(Responsibilities)
                RESPOs.append(json.loads(output_json))
        for Skills in Skills_res['value']:
            if Skills['Code'] == pk:
                output_json = json.dumps(Skills)
                Skill.append(json.loads(output_json))
        for Courses in Courses_res['value']:
            if Courses['Job_ID'] == pk:
                output_json = json.dumps(Courses)
                Course.append(json.loads(output_json))
        for JobMembeship in JobMembeships_res['value']:
            if JobMembeship['Job_ID'] == pk:
                output_json = json.dumps(JobMembeship)
                Member.append(json.loads(output_json))
        for Positions in Positions_res['value']:
            if Positions['Job_ID'] == pk:
                output_json = json.dumps(Positions)
                Position.append(json.loads(output_json))
        for Attachments in Attachments_res['value']:
            if Attachments['Job_ID'] == pk:
                output_json = json.dumps(Attachments)
                Attachment.append(json.loads(output_json))
    except requests.exceptions.ConnectionError as e:
        print(e)
    if request.session['username']:
        my_name = request.session['username']
    else:
        my_name = "John Doe"
    todays_date = datetime.datetime.now().strftime("%b. %d, %Y %A")
    ctx = {"today": todays_date, "res": res,
           "Qualifications": response, "experience": E_response,
           "industry": All_Industry, "member": All_Memberships,
           "RESPOs": RESPOs, "Skill": Skill,
           "Course": Course, "JobMembeship": Member,
           "Position": Position, "Attach": Attachment,
           "my_name": my_name}
    return render(request, 'jobDetail.html', ctx)


def FnApplicantApplyJob(request, pk):
    applicantNo = request.session['No_']
    needCode = ""

    if request.method == 'POST':
        try:
            needCode = request.POST.get('needCode')
        except ValueError:
            messages.error(request, "Invalid credentials, try again")
            return redirect('jobDetail', pk=pk)
    try:
        response = config.CLIENT.service.FnApplicantApplyJob(
            applicantNo, needCode)
        print(response)
        messages.success(request, "Application Sent successfully")
        return redirect('jobDetail', pk=pk)
    except Exception as e:
        messages.error(request, e)
        print(e)
    return redirect('jobDetail', pk=pk)


def FnWithdrawJobApplication(request):
    applicantNo = request.session['No_']
    needCode = ""

    if request.method == 'POST':
        try:
            needCode = request.POST.get('needCode')
        except ValueError:
            messages.error(request, "Invalid credentials, try again")
            return redirect('job')
    try:
        response = config.CLIENT.service.FnWithdrawJobApplication(
            applicantNo, needCode)
        print(response)
        messages.success(request, "Application Cancelled successfully")
        return redirect('job')
    except Exception as e:
        url = redirect('profile')
        messages.error(request, e)
        print(e)
    return redirect('job')
