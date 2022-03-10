# import requests
# from requests_ntlm import HttpNtlmAuth

# username = "fke-admin"
# password = "Administrator#2021!"

# site_url = "http://102.37.117.22:1448/ADMINBC/ODataV4/Company('FKETEST')/UpcomingEvents"

# r = requests.get(site_url, auth=HttpNtlmAuth(username, password))

# print(r.status_code)

# import requests
# from requests_ntlm import HttpNtlmAuth
# import json

# username = "NAVADMIN"
# password = "W3C0d3@llD@y"

# site_url = "http://20.121.189.145:7048/BC140/ODataV4/Company('KMPDC')/Imprests"

# r = requests.get(site_url, auth=HttpNtlmAuth(username, password)).json()

# print(r)


# import requests
# from requests_ntlm import HttpNtlmAuth

# username = "NAVADMIN"
# password = "N@vAdm$n2030!!"

# site_url = "http://13.68.215.64:1248/BC140/ODataV4/Company(%27KMPDC%27)/ProspectiveSuppliercard"

# r = requests.get(site_url, auth=HttpNtlmAuth(username, password))

# print(r.status_code)


from traceback import print_tb
import requests
from requests import Session
from requests_ntlm import HttpNtlmAuth
from zeep import Client
from zeep.transports import Transport
import enum
from datetime import datetime
from requests.auth import HTTPBasicAuth

AUTHS = Session()

WEB_SERVICE_PWD = 'Password@123'
BASE_URL = 'http://20.121.189.145:7047/KMPDC/WS/KMPDC/Codeunit/CuRecruitmentWebPortal'

AUTHS.auth = HTTPBasicAuth('WINNIE', WEB_SERVICE_PWD)
CLIENT = Client(BASE_URL, transport=Transport(session=AUTHS))


# requisitionNo = ''
# lineNo = 0
# itemCode = ""
# location = "AFGHANISTA"
# quantity = 1
# myAction = 'insert'

# response = CLIENT.service.FnStoreRequisitionLine(requisitionNo, lineNo, itemCode, location, quantity,
#                                                  myAction)
# print(response)


# applicantNo = "1"
# lineNo = 0
# qualificationCode = "1"
# sectionLevel = 1
# myAction = "insert"
# response = CLIENT.service.FnApplicantProfessionalCourse(
#     applicantNo, lineNo, qualificationCode, sectionLevel, myAction)
# print(response)

# applicantNo = "1"
# lineNo = 0
# professionalBody = "1"
# membershipNo = 1
# myAction = "insert"
# response = CLIENT.service.FnApplicantProfessionalMembership(
#     applicantNo, lineNo, professionalBody, membershipNo, myAction)
# print(response)

# applicantNo = "1"
# lineNo = 0
# names = "1"
# designation = ""
# company = ""
# address = ""
# telephoneNo = "0791251061"
# email = "enock@gmail.com"
# myAction = "insert"
# response = CLIENT.service.FnApplicantReferee(
#     applicantNo, lineNo, names, designation, company, address, telephoneNo, email, myAction)
# print(response)

applicantNo = "APP-000022"
needCode = "REC0006"
try:
    response = CLIENT.service.FnApplicantApplyJob(applicantNo, needCode)
    print(response)
except Exception as e:
    print(e)
