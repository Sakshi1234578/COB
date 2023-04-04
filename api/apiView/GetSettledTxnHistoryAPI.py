from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import requests
from ..utils.Validation import validate_request_data_empty_string

class GetSettledTxnHistory(APIView):
    def post(self, req):
        try:
            request_fields = ['rpttype', 'noOfClient', 'endDate', 'fromDate', 'clientCode']
            validation_response = validate_request_data_empty_string(request_fields, req.data)
            if not validation_response["status"]:
                 return Response(validation_response, status=status.HTTP_400_BAD_REQUEST)
            url = 'https://reportapi.sabpaisa.in/SabPaisaReport/REST/GetSettledTxnHistory'
            data = requests.post(url, json = req.data)
            return Response(data.json(), status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'message':"Internal Server", "status": status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class getCommonData(APIView):
    def post(self, req):
        try:
            url = 'https://adminapi.sabpaisa.in/SabPaisaAdmin/getDataByCommonProc/getCommonData/0/0'
            data = requests.get(url)
            return Response(data.json())
        except Exception as e:
            print(e)
            return Response({'message':"Internal Server", "status": status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetQFSettledTxnHistory(APIView):
    def post(self, req):
        try:
            url = 'https://reportapi.sabpaisa.in/SabPaisaReport/REST/GetQFSettledTxnHistory'
            data = requests.post(url, json = req.data)
            return Response(data.json(), status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'message':"Internal Server", "status": status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetQFWiseSettledTxnHistory(APIView):
    def post(self, req):
        try:
            url = 'https://reportapi.sabpaisa.in/SabPaisaReport/REST/GetQFWiseSettledTxnHistory'
            data = requests.post(url, json = req.data)
            return Response(data.json(), status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'message':"Internal Server", "status": status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)