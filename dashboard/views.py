from django.shortcuts import render, redirect
import requests
from requests import Session
from requests_ntlm import HttpNtlmAuth
import json
from django.conf import settings as config
import datetime

# Create your views here.


# def canvas(request):
#     if request.method == 'POST':
#         images = request.FILES.getlist('images')
#         for image in images:
#             photo = Photo.objects.create(
#                 image=image,
#             )
#         return redirect('main')
#     return render(request, 'offcanvas.html')


def dashboard(request):
    session = requests.Session()
    session.auth = config.AUTHS

    Access_Point = config.O_DATA.format("/ProcurementMethods")
    year = request.session['years']
    try:
        response = session.get(Access_Point, timeout=10).json()
        OPEN = []
        OPEN_A = []
        RES = []
        RES_A = []
        RFP = []
        RFP_A = []
        RFQ = []
        RFQ_A = []
        EOI = []
        EOI_A = []
        Closed = []
        Active = []
        for tender in response['value']:
            # Open Tender
            if tender['Process_Type'] == 'Tender' and tender['TenderType'] == 'Open Tender':
                output_json = json.dumps(tender)
                OPEN.append(json.loads(output_json))
            if tender['Process_Type'] == 'Tender' and tender['TenderType'] == 'Open Tender' and tender['Status'] == 'New':
                output_json = json.dumps(tender)
                OPEN_A.append(json.loads(output_json))
            # Restricted Tenders
            if tender['Process_Type'] == 'Tender' and tender['TenderType'] == 'Restricted Tender':
                output_json = json.dumps(tender)
                RES.append(json.loads(output_json))
            if tender['Process_Type'] == 'Tender' and tender['TenderType'] == 'Restricted Tender' and tender['Status'] == 'New':
                output_json = json.dumps(tender)
                RES_A.append(json.loads(output_json))
            # RFP
            if tender['Process_Type'] == 'RFP':
                output_json = json.dumps(tender)
                RFP.append(json.loads(output_json))
            if tender['Process_Type'] == 'RFP' and tender['Status'] == 'New':
                output_json = json.dumps(tender)
                RFP_A.append(json.loads(output_json))
            # RFQ
            if tender['Process_Type'] == 'RFQ':
                output_json = json.dumps(tender)
                RFQ.append(json.loads(output_json))
            if tender['Process_Type'] == 'RFQ' and tender['Status'] == 'New':
                output_json = json.dumps(tender)
                RFQ_A.append(json.loads(output_json))
            # EOI
            if tender['Process_Type'] == 'EOI':
                output_json = json.dumps(tender)
                EOI.append(json.loads(output_json))
            if tender['Process_Type'] == 'EOI' and tender['Status'] == 'New':
                output_json = json.dumps(tender)
                EOI_A.append(json.loads(output_json))
            # All
            if tender['Status'] == 'Archived':
                output_json = json.dumps(tender)
                Closed.append(json.loads(output_json))
            if tender['Status'] == 'New':
                output_json = json.dumps(tender)
                Active.append(json.loads(output_json))
        All_O = len(OPEN)
        Active_O = len(OPEN_A)
        RES_Count = len(RES)
        RES_Active = len(RES_A)
        RFP_Count = len(RFP)
        RFP_Active = len(RFP_A)
        RFQ_Count = len(RFQ)
        RFQ_Active = len(RFQ_A)
        EOI_Count = len(EOI)
        EOI_Active = len(EOI_A)
        Close = len(Closed)
        Actives = len(Active)
    except requests.exceptions.ConnectionError as e:
        print(e)
    todays_date = datetime.datetime.now().strftime("%b. %d, %Y %A")
    ctx = {"today": todays_date,
           "All_T": All_O, "Active_O": Active_O,
           "RES": RES_Count,
           "RES_A": RES_Active,
           "RFP": RFP_Count, "RFP_A": RFP_Active,
           "RFQ": RFQ_Count, "RFQ_A": RFQ_Active,
           "EOI": EOI_Count, "EOI_A": EOI_Active,
           "Close": Close, "Actives": Actives, "year": year}
    return render(request, 'main/dashboard.html', ctx)
