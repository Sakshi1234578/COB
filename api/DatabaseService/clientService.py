import traceback

from ..databaseModels.login_master import login_master
from ..databaseModels.client_super_master import client_super_master
from ..databaseModels.merchant_data import merchant_data
from ..databaseModels.lookup_state import lookup_state
from datetime import date
from django.db.models import Q
from ..utils import custom_exceptions
from ..databaseModels.verification import Verification
from ..DatabaseService import category_service
from ..DatabaseService import ZoneMasterDetail
from ..DatabaseService import zoneService
from ..DatabaseService import EmployeeMasterService
from django.db import connection
from ..utils.CustomDictionary import dictfetchall, DictX

def create_profile(data):
    # Should be there check if the profile is already completed or frontend will take care
    merchant = None
    client_code = data.get("clientCode")
    if client_code is not None and client_code != "":
        client = client_super_master.objects.filter(
            clientCode=client_code).first()
        if client:
            raise custom_exceptions.ClientCodeNotCorrect(
                "client code must be unique")
    else:
        raise custom_exceptions.ClientCodeNotCorrect(
            "client code must be provided")
    login_id = data.get("loginId")
    login_data: login_master = login_master.objects.get(loginMasterId=login_id)
    if login_data.master_client_id is not None:
        raise custom_exceptions.ProfileAlreadyCreate("Profile Already Created")
    client_data = client_super_master()
    client_data.clientCode = data.get("clientCode")
    client_data.clientEmail = login_data.email
    client_data.successUrl = "sabpaisa.in"
    client_data.failedUrl = "sabpaisa.in"
    client_data.clientLogoPath = "sabpaisa.in"
    client_data.clientContact = login_data.mobileNumber
    client_data.clientName = login_data.name
    # state_name = data.get('state').upper()

    # if state_name is not None:
    #     try:
    #         state = lookup_state.objects.get(stateName=state_name)
    #         client_data.state_id = state
    #     except Exception as e:
    #         raise custom_exceptions.StateNameNotCorrect(
    #             "Use correct state name")
    try:
        merchant = merchant_data.objects.get(loginMasterId=login_id)
    except merchant_data.DoesNotExist:
        merchant = merchant_data()

    merchant.accountHolderName = data.get("accountHolderName")
    merchant.bankName = data.get("bankName")
    merchant.accountNumber = data.get("accountNumber")
    merchant.ifscCode = data.get("ifscCode")
    merchant.panCard = data.get("pan")
    kyc_data = Verification.objects.get(login_id=login_id)
    merchant.status = kyc_data.status
    merchant.clientCode = data.get("clientCode")
    merchant.clientName = data.get("clientName")
    merchant.loginMasterId = login_data
    merchant.save()

    client_data.merchantId = merchant.merchantId
    client_data.save()

    login_data.master_client_id = client_data
    login_data.save()
    # response_data = ({"clientId": client_data.clientId, "lookupState": state_name, "address": client_data.address,
    response_data = {
        "clientId": client_data.clientId,
        "address": client_data.address,
        "clientAuthenticationType": client_data.clientAuthenticationType,
        "clientCode": client_data.clientCode,
        "clientContact": client_data.clientContact,
        "clientEmail": client_data.clientEmail,
        "clientImagePath": client_data.clientImagePath,
        "clientLink": client_data.clientLink,
        "clientLogoPath": client_data.clientLogoPath,
        "clientName": client_data.clientName,
        "failedUrl": client_data.failedUrl,
        "landingPage": client_data.landingPage,
        "service": client_data.service,
        "successUrl": client_data.successUrl,
        "createdDate": client_data.createdDate,
        "modifiedDate": client_data.modifiedDate,
        "modifiedBy": client_data.modifiedBy,
        "status": client_data.status,
        "reason": client_data.reason,
        "merchantId": merchant.merchantId,
        "requestId": merchant.requestId,
        "clientType": merchant.clientType,
        "parentClientId": merchant.parentClientId,
        "businessType": (merchant.businessType if merchant.businessType else None),
        "pocAccountManager": client_data.pocAccountManager,
        "status": 200,
    }

    return response_data


def update_profile(data):
    login_data = login_master.objects.get(loginMasterId=data.get("loginId"))
    if login_data.master_client_id is None:
        raise custom_exceptions.ProfileNotCreate("Profile is not created")
    user = login_master.objects.filter(
        Q(email=data.get("email")) | Q(username=data.get("email"))
    ).first()
    if user:
        raise custom_exceptions.EmailAlreadyExist("email already exist")
    login_data.mobileNumber = data.get("phone")
    login_data.email = data.get("email")
    client_data = client_super_master.objects.get(
        clientId=login_data.master_client_id.clientId
    )
    client_data.address = data.get("address")
    client_data.clientName = data.get("clientName")
    client_data.clientAuthenticationType = data.get("clientAuthenticationType")
    client_data.clienContact = login_data.mobileNumber
    client_data.email = login_data.email
    client_data.modifiedDate = date.today()
    try:
        state = lookup_state.objects.get(
            Q(stateName=data.get("state")) | Q(stateId=data.get("state"))
        )
        client_data.state_id = state
    except Exception:
        raise custom_exceptions.StateNameNotCorrect("Use correct state name")
    merchant = merchant_data.objects.get(merchantId=client_data.merchantId)
    merchant.bankName = data.get("bankName")
    merchant.accountHolderName = data.get("accountHolderName")
    merchant.accountNumber = data.get("accountNumber")
    merchant.ifscCode = data.get("ifscCode")
    merchant.panCard = data.get("pan")
    client_data.save()
    merchant.save()
    login_data.save()
    return "Updated"


def update_zone_data_by_client_code(
    client_code, risk_category_code, zone_code, zone_head_emp_code, emp_code
):
    try:
        get_client_code = merchant_data.objects.get(clientCode=client_code)
    except Exception:
        traceback.print_exc()
        return "Client Code Not Found"
    get_client_code.risk_category_code = risk_category_code
    get_client_code.zone_code = zone_code
    get_client_code.zone_head_emp_code = zone_head_emp_code
    get_client_code.emp_code = emp_code
    get_client_code.save()
    return "Client Data Updated"


def get_client_code_zone_info(client_code):
    try:
        try:
            get_client_code = merchant_data.objects.get(clientCode=client_code)
        except Exception:
            traceback.print_exc()
            return "Client Code Not Found"
        get_risk_name = category_service.get_category_name(
            get_client_code.risk_category_code
        )
        get_zone_name = zoneService.get_zone_name(get_client_code.zone_code)
        get_zone_head_emp_name = ZoneMasterDetail.get_zone_head_name(
            get_client_code.zone_head_emp_code
        )
        get_emp_name = EmployeeMasterService.get_emp_name(
            get_client_code.emp_code)
        client_data_response = {
            "risk_name": get_risk_name[0][0] if get_risk_name else "NA",
            "zone_name": get_zone_name[0][0] if get_zone_name else "NA",
            "zone_head_name": get_zone_head_emp_name[0][0]
            if get_zone_head_emp_name
            else "NA",
            "employee_name": get_emp_name[0][0] if get_emp_name else "NA",
        }
        return client_data_response
    except Exception:
        traceback.print_exc()
        return "Data Not Found"


def fetch_all_registered_clients(appliactionId):
    sql_query = "SELECT m.merchantId,l.username,l.password,l.last_login_time,l.name,c.client_logo_path, c.client_contact,c.client_code,c.client_name ,c.client_email,c.client_link,c.client_type, c.success_url,c.failed_url,c.bid,c.businessType,c.address,c.state_id,c.parent_client_id, c.status, cam.application_id, cam.client_id , cam.status, cam.configuration_status, cam.subscription_status,cam.created_date,cam.response_date FROM client_application_mapper cam LEFT JOIN client_super_master c ON cam.client_id = c.client_id LEFT JOIN merchant_data m ON c.merchant_id = m.merchantId LEFT JOIN login_master l ON l.login_master_id= m.loginMasterId  WHERE cam.application_id = %s AND cam.status='Verified' and cam.subscription_status ='Subscribed' ORDER BY cam.created_date DESC"
    cursor = connection.cursor()
    cursor.execute(sql_query, [appliactionId])
    row = dictfetchall(cursor)
    client_list = []
    for index in range(len(row)):
        data = DictX(row[index])
        data_list = {
            'merchant_id': data.merchantId,
            'username': data.username,
            'client_password': data.password,
            'last_login_time': data.last_login_time,
            'name': data.name,
            'companyLogoPath': data.client_logo_path,
            'client_contact_person': data.client_contact,
            'client_code': data.client_code,
            'client_username': data.client_name,
            'client_email': data.client_email,
            'client_link': data.client_link,
            'client_type': data.client_type,
            'successUrl': data.success_url,
            'failedUrl': data.failed_url,
            'bid': data.bid,
            'businessType': data.businessType,
            'address': data.address,
            'stateId': data.state_id,
            'stateName': None,
            'parent_client_id': data.parent_client_id,
            'status': data.status,
            'application_id': data.application_id,
            'client_id': data.client_id,
            'configuration_status': data.onfiguration_status,
            'subscription_status': data.subscription_status,
            'Subscribed': data.Subscribed,
            'subscribedTym': data.created_date,
            'responseTym': data.response_date,
            'finalSubscribedTym': data.created_date,
            'finalResponseTym': data.response_date
        }
        client_list.append(data_list)
    return client_list

