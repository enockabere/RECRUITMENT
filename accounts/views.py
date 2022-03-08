import base64
import threading
from django.http import response
from django.shortcuts import redirect, render, HttpResponse
from django.conf import settings as config
import json
import requests
from requests import Session
from requests_ntlm import HttpNtlmAuth
import datetime
from datetime import date
from django.contrib import messages
from cryptography.fernet import Fernet
import re
# Create your views here.


def profile_request(request):

    return render(request, 'profile.html')


def login_request(request):
    todays_date = date.today()
    year = todays_date.year
    session = requests.Session()
    session.auth = config.AUTHS

    Access_Point = config.O_DATA.format("/QyApplicants")

    if request.method == 'POST':

        try:
            email = request.POST.get('email').strip()
            password = str(request.POST.get('password')).strip()
        except ValueError:
            print("Invalid credentials, try again")
            return redirect('login')
        try:
            response = session.get(Access_Point, timeout=10).json()
            for applicant in response['value']:
                if applicant['E_Mail'] == email:
                    res = applicant
        except requests.exceptions.ConnectionError as e:
            print(e)
        Portal_Password = base64.urlsafe_b64decode(res['Portal_Password'])
        cipher_suite = Fernet(config.ENCRYPT_KEY)
        decoded_text = cipher_suite.decrypt(Portal_Password).decode("ascii")
        if decoded_text == password:
            return redirect('dashboard')
        else:
            messages.error(
                request, "Invalid Credentials")
            return redirect('login')
    ctx = {"year": year}
    return render(request, 'login.html', ctx)


def register_request(request):
    todays_date = date.today()
    year = todays_date.year
    email = ''
    password = ''
    confirm_password = ''
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    if request.method == 'POST':
        try:
            email = request.POST.get('email').strip()
            my_password = str(request.POST.get('password')).strip()
            confirm_password = str(
                request.POST.get('confirm_password')).strip()
        except ValueError:
            print("Invalid credentials, try again")
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
    ctx = {"year": year}
    return render(request, "register.html", ctx)
