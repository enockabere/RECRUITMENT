import threading
from django.http import response
from django.shortcuts import redirect, render, HttpResponse
from django.conf import settings as config
import json
import requests
from requests import Session
from requests_ntlm import HttpNtlmAuth
import datetime
from django.urls import reverse
from datetime import date
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from . models import Users
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, force_str, DjangoUnicodeDecodeError
from .utils import generate_token
import secrets
import string
# Create your views here.


def profile_request(request):

    return render(request, 'profile.html')


def login_request(request):
    todays_date = date.today()
    year = todays_date.year
    request.session['years'] = year
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
        except ValueError:
            print("Invalid credentials, try again")
            return redirect('login')
        user = Users.objects.get(email=email)
        if user.email == email and user.password == password:
            return redirect('dashboard')
        else:
            messages.error(
                request, "Invalid Credentials")
            return redirect('login')
    ctx = {"year": year}
    return render(request, 'login.html', ctx)


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


def activate_user(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Users.objects.get(pk=uid)
    except Exception as e:
        user = None
    if user and generate_token.check_token(user, token):
        messages.success(
            request, "Email verified, you can now login")
        return redirect(reverse('login'))
    return render(request, 'activate-failed.html')


def register_request(request):
    todays_date = date.today()
    year = todays_date.year

    firstname = ''
    lastname = ''
    email = ''
    password = ''
    confirm_password = ''
    if request.method == 'POST':
        try:
            firstname = request.POST.get('firstname').strip()
            lastname = request.POST.get('lastname').strip()
            email = request.POST.get('email').strip()
            password = request.POST.get('password').strip()
            confirm_password = request.POST.get('confirm_password').strip()
        except ValueError:
            print("Invalid credentials, try again")
            return redirect('register')
        if len(password) < 6:
            messages.error(request, "Password should be at least 6 characters")
            return redirect('register')
        if password != confirm_password:
            messages.error(request, "Password mismatch")
            return redirect('register')

        user = Users.objects.create(
            firstname=firstname,
            lastname=lastname,
            email=email,
            password=password,
        )
        alphabet = string.ascii_letters + string.digits
        SecretCode = ''.join(secrets.choice(alphabet) for i in range(5))
        request.session['SecretCode'] = SecretCode
        current_site = get_current_site(request)
        email_subject = 'Activate your account'
        email_body = render_to_string('activate.html', {
            "user": user.firstname,
            "domain": current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            "token": generate_token.make_token(user),
            "code": SecretCode
        })
        email = EmailMessage(subject=email_subject, body=email_body,
                             from_email=config.EMAIL_HOST_USER, to=[user.email])
        EmailThread(email).start()
        messages.success(
            request, "We sent you an email to verify your account")
        return redirect('register')
    print(request.session['SecretCode'])
    ctx = {"year": year}
    return render(request, "register.html", ctx)
