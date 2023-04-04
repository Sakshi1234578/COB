from ..DatabaseService import clientService
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from ..utils.Validation import validate_request_data , validate_query_parms
import json
import requests
from ..utils import custom_exceptions


class profile(APIView):
    def post(self, req):
        if req.method == 'POST':
            # request_fields = ["loginId", "clientName", "state", "clientCode", "phone", "accountHolderName",
            #                   "bankName", "accountNumber", "ifscCode", "pan", "clientAuthenticationType", "address"]
            # data = json.loads(req.body.decode("utf-8"))
            # validation_response = validate_request_data(request_fields, data)
            # if not validation_response["status"]:
            #     return Response(validation_response, status=status.HTTP_400_BAD_REQUEST)
            client_data = clientService.create_profile(req.data)
            if client_data:
                return Response(client_data, status=status.HTTP_200_OK)
            else:
                return Response({"message": client_data, "status": status.HTTP_500_INTERNAL_SERVER_ERROR},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, req):
        if req.method == 'PUT':

            request_fields = ["loginId", "clientName", "phone", "email", "state", "accountHolderName", "bankName",
                              "accountNumber", "ifscCode", "pan", "address", "clientAuthenticationType"]
            data = json.loads(req.body.decode("utf-8"))
            validation_response = validate_request_data(request_fields, data)
            if not validation_response["status"]:
                return Response(validation_response, status=status.HTTP_400_BAD_REQUEST)
            data = clientService.update_profile(req.data)
            if data == "Updated":
                return Response({"message": "updated", "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "failed", "status": status.HTTP_500_INTERNAL_SERVER_ERROR},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class clientDetail(APIView):
    def post(self, req):
        clientCode = req.data.get('clientCode')
        res = requests.get(
            "https://securepay.sabpaisa.in/SabPaisa/REST/client/test/getDetailsByClientCode?clientCode=" + str(
                clientCode)).json()
        return Response({"ClientData": res})


class UpdateZoneDataClientCode(APIView):
    def put(self, req):
        client_code = req.data.get('client_code')
        risk_category_code = req.data.get('risk_category_code')
        zone_code = req.data.get('zone_code')
        zone_head_emp_code = req.data.get('zone_head_emp_code')
        emp_code = req.data.get('emp_code')
        request_fields = ["client_code", "risk_category_code", "zone_code", "zone_head_emp_code", "emp_code"]
        validation_response = validate_request_data(request_fields, req.data)
        if not validation_response["status"]:
            return Response(validation_response, status=status.HTTP_400_BAD_REQUEST)
        client_update = clientService.update_zone_data_by_client_code(client_code, risk_category_code, zone_code,
                                                                      zone_head_emp_code, emp_code)
        return Response({"message": client_update, "status": status.HTTP_200_OK},
                        status=status.HTTP_200_OK)


class GetZoneInfoByClientCode(APIView):
    def post(self, req):
        client_code = req.data.get('client_code')
        request_fields = ["client_code"]
        validation_response = validate_request_data(request_fields, req.data)
        if not validation_response["status"]:
            return Response(validation_response, status=status.HTTP_400_BAD_REQUEST)
        client_response = clientService.get_client_code_zone_info(client_code)
        return Response(client_response, status=status.HTTP_200_OK)


class FetchAllRegisteredClients(APIView):
    def post(self, req):
        appliactionId = req.query_params.get('appliactionId')
        request_fields = ['appliactionId']
        validation_response=validate_query_parms(request_fields, req.query_params)
        if not validation_response :
            return Response({"message":"Please provide application ID", "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        data = clientService.fetch_all_registered_clients(appliactionId)
        return Response(data)
        