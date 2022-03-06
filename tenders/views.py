from django.shortcuts import render, redirect
from datetime import date
import requests
from requests import Session
from requests_ntlm import HttpNtlmAuth
import json
from django.conf import settings as config
import datetime
from requests.adapters import HTTPAdapter
from django.contrib import messages

# Create your views here.


def open_tenders(request):
    session = requests.Session()
    session.auth = config.AUTHS
    year = request.session['years']
    Access_Point = config.O_DATA.format("/ProcurementMethods")

    try:
        response = session.get(Access_Point, timeout=10).json()
        open = []
        Submitted = []
        for tender in response['value']:
            if tender['Process_Type'] == 'Tender' and tender['TenderType'] == 'Open Tender' and tender['Status'] == 'New':
                output_json = json.dumps(tender)
                open.append(json.loads(output_json))
            if tender['Process_Type'] == 'Tender' and tender['TenderType'] == 'Open Tender' and tender['Status'] == 'Archived':
                output_json = json.dumps(tender)
                Submitted.append(json.loads(output_json))
    except requests.exceptions.ConnectionError as e:
        print(e)
    count = len(open)
    counter = len(Submitted)
    # Get Timezone
    # creating date object
    todays_date = datetime.datetime.now().strftime("%b. %d, %Y %A")
    ctx = {"today": todays_date, "res": open,
           "count": count, "counter": counter, "sub": Submitted, "year": year}
    return render(request, 'openTenders.html', ctx)


def Open_Details(request, pk):
    session = requests.Session()
    session.auth = config.AUTHS

    year = request.session['years']
    Access_Point = config.O_DATA.format("/ProcurementMethods")
    Access2 = config.O_DATA.format("/ProcurementRequiredDocs")
    lines = config.O_DATA.format("/ProcurementMethodLines")
    res = ''
    State = ''
    try:
        r = session.get(Access2, timeout=7).json()
        response = session.get(Access_Point, timeout=8).json()
        lines_res = session.get(lines, timeout=8).json()
        Open = []
        Doc = []
        Lines = []
        for lines in lines_res['value']:
            if lines['RequisitionNo'] == pk:
                output_json = json.dumps(lines)
                Lines.append(json.loads(output_json))
        for tender in response['value']:
            if tender['No'] == pk:
                output_json = json.dumps(tender)
                Open.append(json.loads(output_json))
                responses = Open
                for my_tender in responses:
                    if my_tender['No'] == pk:
                        res = my_tender
                    if my_tender['Status'] == "New":
                        State = 1
        for docs in r['value']:
            if docs['QuoteNo'] == pk:
                output_json = json.dumps(docs)
                Doc.append(json.loads(output_json))

    except requests.exceptions.ConnectionError as e:
        print(e)

    todays_date = datetime.datetime.now().strftime("%b. %d, %Y %A")
    ctx = {"today": todays_date, "res": res,
           "docs": Doc, "state": State, "line": Lines, "year": year}
    return render(request, "details/open.html", ctx)


def DocResponse(request, pk):
    session = requests.Session()
    session.auth = config.AUTHS
    procurementMethod = ''
    Access_Point = config.O_DATA.format("/ProcurementMethods")
    try:
        response = session.get(Access_Point, timeout=8).json()
        Open = []
        for tender in response['value']:
            if tender['No'] == pk:
                output_json = json.dumps(tender)
                Open.append(json.loads(output_json))
                responses = Open
                for my_tender in responses:
                    if tender['Process_Type'] == 'Tender' and tender['TenderType'] == 'Open Tender':
                        procurementMethod = 1
                    if tender['Process_Type'] == 'Tender' and tender['TenderType'] == "Restricted Tender":
                        procurementMethod = 5
                    if tender['Process_Type'] == 'RFQ':
                        procurementMethod = 2
                    if tender['Process_Type'] == 'EOI':
                        procurementMethod = 4
                    if tender['Process_Type'] == 'RFP':
                        procurementMethod = 3
    except requests.exceptions.ConnectionError as e:
        print(e)
    print(procurementMethod)
    vendNo = '01254796'
    docNo = pk
    unitPrice = ''
    if request.method == "POST":
        try:
            unitPrice = float(request.POST.get('amount'))
            messages.success(
                request, f"You have successfully Applied for Doc number {docNo}")
        except ValueError:
            messages.error(request, "Invalid Amount, Try Again!!")
            return redirect('Odetails', pk=docNo)
    try:
        if vendNo != '':
            result = config.CLIENT.service.FnCreateProspectiveSupplier(
                vendNo, procurementMethod, docNo, unitPrice)
            print(result)
            return redirect('Odetails', pk=docNo)
    except Exception as e:
        messages.error(request, e)
        print(e)
    return redirect('Odetails', pk=docNo)


def Restricted_tenders(request):
    session = requests.Session()
    session.auth = config.AUTHS
    year = request.session['years']
    Access_Point = config.O_DATA.format("/ProcurementMethods")
    try:
        response = session.get(Access_Point, timeout=10).json()
        Restrict = []
        Submitted = []
        for tender in response['value']:
            if tender['Process_Type'] == 'Tender' and tender['TenderType'] == "Restricted Tender" and tender['Status'] == 'New':
                output_json = json.dumps(tender)
                Restrict.append(json.loads(output_json))
            if tender['Process_Type'] == 'Tender' and tender['TenderType'] == "Restricted Tender" and tender['Status'] == 'Archived':
                output_json = json.dumps(tender)
                Submitted.append(json.loads(output_json))
    except requests.exceptions.ConnectionError as e:
        print(e)

    count = len(Restrict)
    counter = len(Submitted)

    todays_date = datetime.datetime.now().strftime("%b. %d, %Y %A")
    ctx = {"today": todays_date, "res": Restrict,
           "count": count, "sub": Submitted, "counter": counter, "year": year}
    return render(request, 'restrictedTenders.html', ctx)
