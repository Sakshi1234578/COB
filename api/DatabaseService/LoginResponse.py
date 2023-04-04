from ..databaseModels.login_master import login_master
from django.db import connection
from api.databaseModels.merchant_data import merchant_data
from api.databaseModels.client_super_master import client_super_master
from ..utils.CustomDictionary import dictfetchall, DictX


def login_response(username, password):
    client_super_master_list = None
    cursor = connection.cursor()
    login_master_data = login_master.objects.filter(username=username, password=password).first()
    res = {
        "loginId": login_master_data.loginMasterId, "userName": login_master_data.username,
        "clientContactPersonName": login_master_data.name or None, "clientEmail": login_master_data.email,
        "clientMobileNo": login_master_data.mobileNumber or None,
        "roleId": (login_master_data.roleId.roleId if login_master_data.roleId.roleId else None) if (
            login_master_data.roleId) else None,
        "loginMessage": "success", "roleName": ((login_master_data.roleId.roleName) if (
            login_master_data.roleId.roleName) else None) if login_master_data.roleId else None,
        "createDate": login_master_data.createdDate or None,
        "requestId": login_master_data.requestId or None,             
        "isDirect": login_master_data.isDirect if (login_master_data.isDirect or login_master_data.isDirect==False) else None,
        "loginStatus": login_master_data.status,
    }
    if login_master_data.roleId.roleId == 1:
        return admin_login_data(cursor, res)

    elif login_master_data.roleId.roleId == 3:
        return bank_login_data(cursor, login_master_data, res)

    elif login_master_data.roleId.roleId == 13:
        return reseller_login_data(login_master_data, res)

    else:
        merchant = None
        client_list = []
        try:
            merchant = merchant_data.objects.get(loginMasterId=login_master_data.loginMasterId)
        except Exception as e:
            merchant = None
        if merchant:
            
            try:
                client_super_master_list = client_super_master.objects.get(merchantId=merchant.merchantId)
            except Exception as e:
                b = {
                    "clientId": None,
                    "clientCode": None,
                    "clientType": None,
                    "address": None,
                    "stateName": None,
                    "stateId": None,
                    "business_cat_code": login_master_data.business_cat_code,
                    "clientName": login_master_data.name,
                    "clientEmail": login_master_data.email,
                    "roleType": (
                        (login_master_data.roleId.roleName) if (login_master_data.roleId.roleName) else (None)) if (
                        login_master_data.roleId) else None,
                    "clientUserName": login_master_data.username or None,
                    "lastLoginTime": login_master_data.lastLoginTime or None
                }
                client_list.append(b)
                res["clientMerchantDetailsList"] = client_list
                return res
            b = {
                "clientId": client_super_master_list.clientId or None,
                "clientCode": client_super_master_list.clientCode or None,
                "clientName": client_super_master_list.clientName or None,
                "clientContact": client_super_master_list.clientContact or None,
                "clientEmail": client_super_master_list.clientEmail or None,
                "business_cat_code": login_master_data.business_cat_code or None,
                "roleType": (
                    (login_master_data.roleId.roleName) if (login_master_data.roleId.roleName) else (None)) if (
                    login_master_data.roleId) else None,
                "clientUserName": login_master_data.username or None,
                "clientType": client_super_master_list.clientType or None,
                "lastLoginTime": login_master_data.lastLoginTime or None,
                "address": client_super_master_list.address or None,
                "stateName": (
                    (client_super_master_list.state_id.stateName) if (
                        client_super_master_list.state_id.stateName) else (
                        None)) if (client_super_master_list.state_id) else None,
                "stateId": (
                    (client_super_master_list.state_id.stateId) if (
                        client_super_master_list.state_id.stateId) else (
                        None)) if (client_super_master_list.state_id) else None,
            }
            client_list.append(b)
            res["clientMerchantDetailsList"] = client_list
            res['accountHolderName'] = merchant.accountHolderName or None
            res['bankName'] = merchant.bankName or None
            res['accountNumber'] = merchant.accountNumber or None
            res['ifscCode'] = merchant.ifscCode or None
            res['state'] = client_list[0]['stateName']
            res['pan'] = merchant.panCard or None
            res['merchantDataStatus'] = merchant.status or None
            res['clientAuthenticationType'] = client_super_master_list.clientAuthenticationType or None
        else:
            b = {
                "clientId": ((
                                 login_master_data.master_client_id.clientId if login_master_data.master_client_id else None) if login_master_data.master_client_id else None),
                "clientCode": None,
                "clientType": None,
                "address": None,
                "stateName": None,
                "stateId": None,
                "clientName": login_master_data.name,
                "clientEmail": login_master_data.email,
                "roleType": (
                    (login_master_data.roleId.roleName) if (login_master_data.roleId.roleName) else (None)) if (
                    login_master_data.roleId) else None,
                "clientUserName": login_master_data.username or None,
                "lastLoginTime": login_master_data.lastLoginTime or None,
                "business_cat_code": login_master_data.business_cat_code or None,
            }
            client_list.append(b)
            res["clientMerchantDetailsList"] = client_list
        return res


def reseller_login_data(login_master_data, res):
    referrer_clients = client_super_master.objects.filter(requestId=login_master_data.requestId)
    login_id = []
    for client in referrer_clients.iterator():
        referrer_login = merchant_data.objects.get(merchantId=client.merchantId)
        login_id.append(referrer_login.loginMasterId.loginMasterId)
    client_list = []
    count = 0
    for client in referrer_clients.iterator():
        b = {
            'loginId': login_id[count],
            "clientId": client.clientId,
            "clientCode": client.clientCode,
            "clientName": client.clientName,
            "clientContact": client.clientContact,
            "clientEmail": client.clientEmail,
            "roleType": "Client",
            "clientType": client.clientType,
            "parentClientId": client.parentClientId
        }
        client_list.append(b)
        count += 1
    res['clientMerchantDetailsList'] = client_list
    return res


def bank_login_data(cursor, login_master_data, res):
    # Inside Bank
    sql_query = "SELECT c.client_id ,c.client_code ,c.client_contact,c.client_name,c.address,b.bank_id, m.loginMasterId FROM bank_master b left join client_super_master c on c.bid = b.bank_id left join merchant_data m on m.merchantId = c.merchant_id  where b.loginId=%s and m.onBoardFrom ='Bank Client' and c.client_type!='child client' order by c.client_name asc"
    cursor.execute(sql_query, [login_master_data.loginMasterId])
    row = dictfetchall(cursor)
    client_merchant_list = []
    for index in range(len(row)):
        data = DictX(row[index])
        data_list = {
            'loginId': data.loginMasterId,
            'ClientId': data.client_id,
            'clientCode': data.client_code,
            'clientName': data.client_name,
            'clientContact': data.client_contact,
            'clientEmail': data.client_email,
            'clientUserName': data.client_user_name,
            'roleType': "Client"
        }
        client_merchant_list.append(data_list)
    res['clientMerchantDetailsList'] = client_merchant_list
    return res


def admin_login_data(cursor, res):
    # Inside Admin
    sql_query = "SELECT m.merchantId,l.login_master_id,l.username,l.password,l.last_login_time, l.name ," \
                "c.client_logo_path, c.client_contact,c.client_code,c.client_name ,c.client_id,c.client_email," \
                "c.client_link,c.client_type, c.success_url,c.failed_url,c.bid,c.businessType,c.address," \
                "c.state_id,c.parent_client_id,c.status, cam.application_id, cam.client_id , cam.status, " \
                "cam.configuration_status,cam.subscription_status,cam.created_date,cam.response_date FROM " \
                "client_application_mapper cam LEFT JOIN client_super_master c ON cam.client_id = c.client_id  " \
                "LEFT JOIN merchant_data m ON c.merchant_id = m.merchantId LEFT JOIN login_master l ON  " \
                "l.login_master_id= m.loginMasterId  WHERE cam.application_id=%s AND cam.status='Verified' and " \
                "cam.subscription_status ='Subscribed' ORDER BY cam.created_date DESC "
    cursor.execute(sql_query, [3])
    row = dictfetchall(cursor)
    client_merchant_list = []
    for index in range(len(row)):
        data = DictX(row[index])
        data_list = {
            'loginId': data.login_master_id,
            'ClientId': data.client_id,
            'clientCode': data.client_code,
            'clientName': data.client_name,
            'clientContact': data.client_contact,
            'clientEmail': data.client_email,
            'clientContactPerson': data.client_contact,
            'clientUsername': data.username,
            'lastLoginTime': data.last_login_time,
            'roleType': "Client",
            'clientType': data.client_type,
            'parentClientId': data.parent_client_id,
            'address': data.address,
            'stateId': data.state_id,
            'bid': data.bid,
            'businessType': data.businessType,
            'successUrl': data.success_url,
            'failedUrl': data.failed_url,
            'subscriptionStatus': data.subscription_status,
            'configuration_status': data.configuration_status
        }
        client_merchant_list.append(data_list)
    res['clientMerchantDetailsList'] = client_merchant_list
    return res

# def login_response_normal_mearchant(data)
