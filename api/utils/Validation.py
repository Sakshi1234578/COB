import requests

def validate_query_parms(fields: list, query_params):
    for key in fields:
        if not  (key in query_params and query_params[key]):
            return {"status": False, "message": key + " is missing"}
    return {"status": True, "message": "Data validated successfully"}

def validate_request_data(fields: list, request_data):
    for key in fields:
        if not  (key in request_data and request_data[key]):
            return {"status": False, "message": key + " is missing"}
    return {"status": True, "message": "Data validated successfully"}


def validate_request_data_empty_string(fields: list, request_data):
    for key in fields:
        if not (key in request_data):
            return {"status": False, "message": key + " is missing"}
    return {"status": True, "message": "Data validated successfully"}


def send_request(url, data, headers=None, type=None):
    headers['Content-Type'] = 'application/json'
    print("sending request...")
    if type == 'POST':
        res = requests.post(url, json=data, headers=headers)
    elif type == 'GET':
        res = requests.get(url, json=data, headers=headers)
    print("request sent")
    return res

    