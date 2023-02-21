import base64
import logging
import threading
import aiohttp
from django.shortcuts import redirect, render
from django.conf import settings as config
import json
from django.views import View
import requests
import datetime
from datetime import datetime
from django.contrib import messages
from cryptography.fernet import Fernet
from myRequest.views import UserObjectMixins
import asyncio
from asgiref.sync import sync_to_async
import enum
from django.http import JsonResponse
# Create your views here.


def login_request(request):
    session = requests.Session()
    session.auth = config.AUTHS

    Access_Point = config.O_DATA.format("/QyApplicants")
    username = ''
    Portal_Password = ""
    if request.method == 'POST':

        try:
            email = request.POST.get('email').strip()
            password = request.POST.get('password')
        except ValueError:
            messages.error(request, "Invalid credentials, try again")
            return redirect('login')
        try:
            response = session.get(Access_Point, timeout=10).json()
            for applicant in response['value']:
                if applicant['E_Mail'] == email:
                    try:
                        Portal_Password = base64.urlsafe_b64decode(
                            applicant['Portal_Password'])
                        request.session['No_'] = applicant['No_']
                        request.session['E_Mail'] = applicant['E_Mail']
                        request.session['full_name'] = applicant['First_Name'] + " " + applicant['Last_Name']

                    except Exception as e:
                        messages.error(request, e)
                        return redirect('login')
        except requests.exceptions.ConnectionError as e:
            print(e)

        cipher_suite = Fernet(config.ENCRYPT_KEY)
        try:
            decoded_text = cipher_suite.decrypt(
                Portal_Password).decode("ascii")
        except Exception as e:
            messages.error(request, e)
            return redirect('login')
        if decoded_text == password:
            return redirect('dashboard')
        else:
            messages.error(
                request, "Invalid Credentials")
            return redirect('login')
    ctx = { "username": username}
    return render(request, 'login.html', ctx)


def register_request(request):
    password = ''
    confirm_password = ''

    if request.method == 'POST':
        try:
            email = request.POST.get('email').strip()
            my_password = str(request.POST.get('password'))
            confirm_password = str(
                request.POST.get('confirm_password')).strip()
        except ValueError:
            messages.error(request, "Invalid credentials, try again")
            return redirect('register')
        if len(my_password) < 6:
            messages.error(request, "Password should be at least 6 characters")
            return redirect('register')
        if my_password != confirm_password:
            messages.error(request, "Password mismatch")
            return redirect('register')
        cipher_suite = Fernet(config.ENCRYPT_KEY)

        encrypted_text = cipher_suite.encrypt(my_password.encode('ascii'))
        password = base64.urlsafe_b64encode(encrypted_text).decode("ascii")

        try:
            response = config.CLIENT.service.FnApplicantRegister(
                email, password)
            messages.success(
                request, "Account successfully created, you can now login")
            print(response)
            return redirect('login')
        except Exception as e:
            messages.error(request, e)
            print(e)
    ctx = {}
    return render(request, "register.html", ctx)


class FnApplicantDetails(UserObjectMixins,View):
    def post(self,request):
        try:
            applicantNo = request.session['No_']
            disabilityGrade = 0
            firstName = request.POST.get('firstName')
            middleName = request.POST.get('middleName')
            lastName = request.POST.get('lastName')
            idNumber = request.POST.get('idNumber')
            genders = request.POST.get('gender')
            citizenship = request.POST.get('citizenship')
            countyCode = request.POST.get('countyCode')
            maritalStatus = int(request.POST.get('maritalStatus'))
            ethnicOrigin = int(request.POST.get('ethnicOrigin'))
            disabled = int(request.POST.get('disabled'))
            dob = request.POST.get('dob')
            phoneNumber = request.POST.get('phoneNumber')
            postalAddress = request.POST.get('postalAddress')
            postalCode = request.POST.get('postalCode')
            residentialAddress = request.POST.get('residentialAddress')
            disabilityGrade = request.POST.get('disabilityGrade')
            if not countyCode:
                countyCode = ""
                
            if not disabilityGrade:
                disabilityGrade = 0
            class Data(enum.Enum):
                values = genders
            gender = (Data.values).value

            response = self.make_soap_request('FnApplicantDetails',
                                              applicantNo, firstName,
                                                middleName, lastName,
                                                    idNumber, gender,
                                                        citizenship,
                                                            countyCode, maritalStatus,
                                                                ethnicOrigin, disabled, dob,
                                                                    phoneNumber, postalAddress,
                                                                        postalCode, residentialAddress,
                                                                            int(disabilityGrade))
            if response == True:
                messages.success(request, "Successfully Added")
                return redirect('profile')
        except Exception as e:
            messages.error(request, f'{e}')
            logging.exception(e)
            return redirect('profile')


class profile_request(UserObjectMixins, View):
    async def get(self, request):
        try:
            applicantNo = await sync_to_async(request.session.__getitem__)('No_')
            full_name = await sync_to_async (request.session.__getitem__)('full_name')
            personal_info = {}
            country = []
            tribes = []
            Study = []
            qualifications = []
            ctx = {}
            industry = []
            Bodies = []

            async with aiohttp.ClientSession() as session:
                personal_details = asyncio.ensure_future(self.simple_one_filtered_data(session,
                                                                                       '/QyApplicants',
                                                                                       "No_", 'eq',
                                                                                       applicantNo))
                get_country = asyncio.ensure_future(self.simple_fetch_data(session,
                                                                '/CountryRegion'))
                # change this query to the one for tribes
                get_tribes = asyncio.ensure_future(self.simple_fetch_data(session,
                                                                    '/QyCounties'))
                field_of_study = asyncio.ensure_future(self.simple_fetch_data(session,
                                                                              '/QyFieldsOfStudy'))
                
                qualifications = asyncio.ensure_future(self.simple_fetch_data(session,
                                                                              '/QyQualificationCodes'))
                
                job_industries = asyncio.ensure_future(self.simple_fetch_data(session,
                                                                            '/QyJobIndustries'))
                
                pro_bodies = asyncio.ensure_future(self.simple_fetch_data(session,
                                                                          '/QyProfessionalBodies'))
                
                response = await asyncio.gather(personal_details,get_country,
                                                get_tribes,field_of_study,qualifications,
                                                    job_industries,pro_bodies)
                
                for data in response[0]:
                    personal_info = data
                country =[country for country in response[1]]
                tribes = [tribe for tribe in response[2]]
                Study = [study for study in response[3]]
                qualifications = [qualification for qualification in response[4]]
                industry = [industry for industry in response[5]]
                Bodies = [body for body in response[6]]

            ctx = {
                "applicant": personal_info,
                "country": country,
                'tribes':tribes,
                'qualifications':qualifications,
                'Study':Study,
                'industry':industry,
                'pro_bodies':Bodies,
                "my_name": full_name,
            }

        except KeyError:
            messages.error(request, "Session has expired, Login Again")
            return redirect('login')
        except Exception as e:
            messages.error(request, f'{e}')
            print(e)
            return redirect('dashboard')
        return render(request, 'profile.html', ctx)
    
class Counties(UserObjectMixins,View):
    def get(self,request):    
        try:
            counties = self.get_object('/QyCounties')
            return JsonResponse(counties, safe=False)

        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, safe=False)
        
class AcademicQualifications(UserObjectMixins,View):
    def get(self,request):    
        try:
            Applicant_No_ = request.session['No_']
            qualifications = self.one_filter('/QyApplicantAcademicQualifications',
                                                'Applicant_No_',"eq",Applicant_No_)
           
            return JsonResponse(qualifications, safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, safe=False)

class QyApplicantJobExperience(UserObjectMixins,View):
    def get(self,request):    
        try:
            Applicant_No_ = request.session['No_']
            experience = self.one_filter('/QyApplicantJobExperience',
                                                'Applicant_No_',"eq",Applicant_No_)
            
            return JsonResponse(experience, safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, safe=False)
        
class QyApplicantJobProfessionalCourses(UserObjectMixins,View):
    def get(self,request):    
        try:
            Applicant_No_ = request.session['No_']
            pro_courses = self.one_filter('/QyApplicantJobProfessionalCourses',
                                                'Applicant_No_',"eq",Applicant_No_)
                        
            return JsonResponse(pro_courses, safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, safe=False)
class QyApplicantProfessionalMemberships(UserObjectMixins,View):
    def get(self,request):    
        try:
            Applicant_No_ = request.session['No_']
            pro_memberships = self.one_filter('/QyApplicantProfessionalMemberships',
                                                'Applicant_No_',"eq",Applicant_No_)
                        
            return JsonResponse(pro_memberships, safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, safe=False)
        
class QyApplicantHobbies(UserObjectMixins,View):
    def get(self,request):    
        try:
            Applicant_No_ = request.session['No_']
            hobbies = self.one_filter('/QyApplicantHobbies',
                                                'No_',"eq",Applicant_No_)
                        
            return JsonResponse(hobbies, safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, safe=False)
        
class QyApplicantReferees(UserObjectMixins,View):
    def get(self,request):    
        try:
            Applicant_No_ = request.session['No_']
            referees = self.one_filter('/QyApplicantReferees',
                                                'No',"eq",Applicant_No_)
                        
            return JsonResponse(referees, safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, safe=False)


class JobExperience(UserObjectMixins,View):
    def post(self,request):
        try:
            applicantNo = request.session['No_']
            lineNo = 0
            myAction = "insert"
            startDate  = datetime.strptime(request.POST.get('startDate'), '%Y-%m-%d').date()
            startDate = request.POST.get('startDate')
            endDate = request.POST.get('endDate')
            employer = request.POST.get('employer')
            industry = request.POST.get('industry')
            hierarchyLevels = request.POST.get('hierarchyLevel')
            functionalArea = request.POST.get('functionalArea')
            jobTitle = request.POST.get('jobTitle')
            isPresentEmployment = request.POST.get('isPresentEmployment')
            country = request.POST.get('country')
            description = request.POST.get('description')
            location = request.POST.get('location')
            employerEmail = request.POST.get('employerEmail')
            employerPostalAddress = request.POST.get('employerPostalAddress')
            
            if not endDate:
                endDate = '0001-01-01'
                
            endDate = datetime.strptime(endDate, '%Y-%m-%d').date()

            class Data(enum.Enum):
                values = hierarchyLevels

            hierarchyLevel = (Data.values).value
            response = self.make_soap_request('FnApplicantJobExperience',
                                              applicantNo, lineNo, startDate,
                                                    endDate, employer, industry, hierarchyLevel, 
                                                    functionalArea, jobTitle,
                                                        isPresentEmployment, country, description,
                                                        location, employerEmail, 
                                                        employerPostalAddress,
                                                        myAction)
            return JsonResponse(response, safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, safe=False)


class FnApplicantProfessionalCourse(UserObjectMixins,View):
    def post(self,request):
        try:
            qualificationCode = request.POST.get('qualificationCode')
            sectionLevel = int(request.POST.get('sectionLevel'))
            otherQualification = request.POST.get('otherQualification')
            applicantNo = request.session['No_']
            lineNo = 0
            myAction = "insert"
            if not otherQualification:
                otherQualification = ''

            response = self.make_soap_request('FnApplicantProfessionalCourse',
                            applicantNo, lineNo, qualificationCode, sectionLevel,
                            myAction, otherQualification)
            return JsonResponse(response, safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, safe=False)


class FnApplicantAcademicQualification(UserObjectMixins,View):
    def post(self,request):
        try:
            applicantNo = request.session['No_']
            lineNo = 0
            myAction = "insert"
            startDate = request.POST.get('startDate')
            endDate = request.POST.get('endDate')
            educationTypes = request.POST.get('educationType')
            educationLevels = request.POST.get('educationLevel')
            fieldOfStudy = request.POST.get('fieldOfStudy')
            qualificationCode = request.POST.get('qualificationCode')
            institutionName = request.POST.get('institutionName')
            proficiencyLevels = request.POST.get('proficiencyLevel')
            country = request.POST.get('country')
            isHighestLevel = request.POST.get('isHighestLevel')
            description = request.POST.get('description')
            grade = request.POST.get('grade')
            otherQualification = request.POST.get('otherQualification')

            class Data(enum.Enum):
                values = educationTypes
                education = educationLevels
                proficiency = proficiencyLevels

            educationType = (Data.values).value
            educationLevel = (Data.education).value
            proficiencyLevel = (Data.proficiency).value

            response = self.make_soap_request('FnApplicantAcademicQualification',
                                                applicantNo, lineNo, startDate,
                                                    endDate, educationType, educationLevel, 
                                                        fieldOfStudy, qualificationCode, institutionName,
                                                            proficiencyLevel, country, isHighestLevel,
                                                                description, grade, myAction, otherQualification)

            return JsonResponse({'response':response})
        except Exception as e:
            messages.error(request, f'{e}')
            logging.exception(e)
            return redirect('profile')


class FnApplicantProfessionalMembership(UserObjectMixins,View):
    def post(self,request):
        try:
            applicantNo = request.session['No_']
            lineNo = 0
            myAction = "insert"
            professionalBody = request.POST.get('professionalBody')
            membershipNo = request.POST.get('membershipNo')
            otherProfessionalBody = request.POST.get('otherProfessionalBody')
            
            if not otherProfessionalBody:
                otherProfessionalBody = ''

            response = self.make_soap_request('FnApplicantProfessionalMembership',
                                    applicantNo, lineNo, professionalBody, membershipNo,
                                    myAction, otherProfessionalBody)
            print(response)
            return JsonResponse(response, safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, safe=False)


class FnApplicantHobby(UserObjectMixins,View):
    def post(self,request):
        try:
            applicantNo = request.session['No_']
            lineNo = 0
            myAction = "insert"
            hobby = request.POST.get('hobby')

            response = self.make_soap_request('FnApplicantHobby',
                applicantNo, lineNo, hobby, myAction)
            print(response)
            return JsonResponse(response, safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, safe=False)


class FnApplicantReferee(UserObjectMixins,View):
    def post(self,request):
        try:
            applicantNo = request.session['No_']
            lineNo = 0
            names = request.POST.get('names')
            designation = request.POST.get('designation')
            company = request.POST.get('company')
            telephoneNo = request.POST.get('telephoneNo')
            email = request.POST.get('email')
            myAction = "insert"
            response = self.make_soap_request('FnApplicantReferee',
                            applicantNo, lineNo, names, designation,
                            company, telephoneNo, email, myAction)
            
            return JsonResponse(response, safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, safe=False)



def logout(request):
    try:
        del request.session['No_']
        del request.session['E_Mail']
        messages.success(request, 'Logged out successfully')
    except KeyError:
        print(False)
    return redirect('login')
