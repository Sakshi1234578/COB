from django.db import connection
from ..utils.CustomDictionary import dictfetchall, DictX
from ..utils import custom_exceptions


def BankDetails(BankID, stateID):
    cursor = connection.cursor()
    # check the condition if state id is not null
    
    if stateID:
        sql_query1 = '''SELECT c.bid, c.client_email, c.client_contact,  l.state_code, c.client_id,c.client_code, c.client_name, c.application_url FROM bank_master b left join client_super_master c on c.bid = 
    b.bank_id left join merchant_data m on m.merchantId = c.merchant_id left join lookup_state l on l.state_id = c.state_id  where c.bid=%s and c.state_id=%s  and
    m.onBoardFrom ='Bank Client' and c.client_type!='child client' order by c.client_name asc'''
        cursor.execute(sql_query1, [BankID, stateID])
    else: 
        sql_query1 = '''SELECT c.bid, c.client_email, c.client_contact, l.state_code, c.client_id,c.client_code, c.client_name, c.application_url FROM bank_master b left join client_super_master c on c.bid = 
    b.bank_id left join merchant_data m on m.merchantId = c.merchant_id left join lookup_state l on l.state_id = c.state_id  where c.bid=%s  and
    m.onBoardFrom ='Bank Client' and c.client_type!='child client' order by c.client_name asc'''
        cursor.execute(sql_query1, [BankID])
        
    
    row = dictfetchall(cursor)

    Bank_detail_list = []
    for index in range(len(row)):
        data = DictX(row[index])

        data_list = {
            'clientId': data.client_id if data.client_id else "NA",
            'clientCode': data.client_code if data.client_code else "NA",
            'clientName': data.client_name if data.client_name else "NA",
            "clientAppURL": data.application_url if data.application_url else "NA",
            'BankId': data.bid if data.bid else "NA",
            'clientEmailID': data.client_email if data.client_email else "NA",
            'clientMobileNo': data.client_contact if data.client_contact else "NA",
            'stateCode': data.state_code if data.state_code else "NA"
        }
        Bank_detail_list.append(data_list)
    return Bank_detail_list