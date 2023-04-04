from ..DatabaseService.BankDetailsService import BankDetails
from rest_framework.views import APIView
from ..utils import custom_exceptions
from rest_framework import status
from rest_framework.response import Response



class BankDetail(APIView):
    def post(self, req):
        if req.data.get('BankID') ==None or req.data.get('BankID')=="":
           raise custom_exceptions.IncompleteDataException("Please provide bankID")
        if req.data.get('stateID')!=None and req.data.get('stateID')!="":
            if not req.data.get('BankID').isnumeric() or not req.data.get('stateID').isnumeric():
                raise custom_exceptions.IntegerFieldRequired("Please send numeric value in bankID and stateId")
        else: 
            if not req.data.get('BankID').isnumeric():
                raise custom_exceptions.IntegerFieldRequired("Please send numeric value in bankID")
        stateId = req.data.get('stateID')
        if  stateId == "":
            stateId = None
        data=BankDetails(req.data.get('BankID'), stateId)
        return Response({"BankDetails":data, "status": status.HTTP_200_OK}, status=status.HTTP_200_OK) 
        
            

