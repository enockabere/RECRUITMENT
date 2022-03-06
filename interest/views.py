from django.shortcuts import render, redirect
from datetime import date
import requests
from requests import Session
from requests_ntlm import HttpNtlmAuth
import json
from django.conf import settings as config
import datetime
from django.contrib import messages

# Create your views here.


def interest_request(request):
    session = requests.Session()
    session.auth = config.AUTHS

    year = request.session['years']
    Access_Point = config.O_DATA.format("/ProcurementMethods")
    try:
        response = session.get(Access_Point, timeout=10).json()
        OpenEOI = []
        Submitted = []
        for tender in response['value']:
            if tender['Process_Type'] == 'EOI' and tender['Status'] == 'New':
                output_json = json.dumps(tender)
                OpenEOI.append(json.loads(output_json))
            if tender['Process_Type'] == 'EOI' and tender['Status'] == 'Archived':
                output_json = json.dumps(tender)
                Submitted.append(json.loads(output_json))
    except requests.exceptions.ConnectionError as e:
        print(e)

    count = len(OpenEOI)
    counter = len(Submitted)
    # Get Timezone
    # creating date object
    todays_date = datetime.datetime.now().strftime("%b. %d, %Y %A")
    ctx = {"today": todays_date, "res": OpenEOI,
           "count": count, "sub": Submitted,
           "year": year, "counter": counter}
    return render(request, 'interest.html', ctx)
