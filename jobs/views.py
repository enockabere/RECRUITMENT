from django.shortcuts import render, redirect
import requests
from requests import Session
from requests_ntlm import HttpNtlmAuth
import json
from django.conf import settings as config
import datetime

# Create your views here.


def CompanyJobs(request):
    session = requests.Session()
    session.auth = config.AUTHS

    Access_Point = config.O_DATA.format("/QyCompanyJobs")
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
    return render(request, 'job.html', ctx)
