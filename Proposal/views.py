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


def proposal_request(request):
    session = requests.Session()
    session.auth = config.AUTHS

    year = request.session['years']
    Access_Point = config.O_DATA.format("/ProcurementMethods")
    try:
        response = session.get(Access_Point, timeout=10).json()
        OpenRFP = []
        Submitted = []
        for tender in response['value']:
            if tender['Process_Type'] == 'RFP' and tender['Status'] == 'New':
                output_json = json.dumps(tender)
                OpenRFP.append(json.loads(output_json))
            if tender['Process_Type'] == 'RFP' and tender['Status'] == 'Archived':
                output_json = json.dumps(tender)
                Submitted.append(json.loads(output_json))
    except requests.exceptions.ConnectionError as e:
        print(e)
    count = len(OpenRFP)
    counter = len(Submitted)
    # Get Timezone
    # creating date object
    todays_date = datetime.datetime.now().strftime("%b. %d, %Y %A")
    ctx = {"today": todays_date, "res": OpenRFP,
           "count": count, "counter": counter,
           "year": year, "sub": Submitted}
    return render(request, 'proposal.html', ctx)
