from rest_framework import status
from ..DatabaseService import merchant_service
from rest_framework.views import APIView
from rest_framework.response import Response
from ..utils import custom_exceptions
from ..utils.Validation import validate_request_data
from datetime import datetime
import requests


class RateTemplateMaster(APIView):
    def post(self, req):
        risk_cat_code = req.data.get('risk_cat_code')
        request_fields = ['risk_cat_code']
        validation_response = validate_request_data(request_fields, req.data)
        if not validation_response["status"]:
            return Response(validation_response, status=status.HTTP_400_BAD_REQUEST)
        template_master_response = merchant_service.get_rate_template_data(risk_cat_code)
        if template_master_response:
            return Response(template_master_response, status=status.HTTP_200_OK)
        else:
            raise custom_exceptions.DataNotFound("Data Not Found")


class TemplateMasterByBusinessCode(APIView):
    def post(self, req):
        business_cat_code = req.data.get('business_cat_code')
        request_fields = ['business_cat_code']
        validation_response = validate_request_data(request_fields, req.data)
        if not validation_response["status"]:
            return Response(validation_response, status=status.HTTP_400_BAD_REQUEST)
        template_master_response = merchant_service.get_template_data_by_business_code(business_cat_code)
        if template_master_response:
            return Response(template_master_response, status=status.HTTP_200_OK)
        else:
            raise custom_exceptions.DataNotFound("Data Not Found")


class RiskCatgTemplateNameByCode(APIView):
    def post(self, req):
        rate_template_code = req.data.get('rate_template_code')
        business_cat_code = req.data.get('business_cat_code')
        risk_cat_code = req.data.get('risk_cat_code')
        request_fields = ['rate_template_code', 'business_cat_code', 'risk_cat_code']
        validation_response = validate_request_data(request_fields, req.data)
        if not validation_response["status"]:
            return Response(validation_response, status=status.HTTP_400_BAD_REQUEST)
        template_data_res = merchant_service.get_risk_template_data_by_code(rate_template_code, business_cat_code,
                                                                            risk_cat_code)
        if template_data_res:
            return Response(template_data_res, status=status.HTTP_200_OK)
        else:
            raise custom_exceptions.DataNotFound("Data Not Found")


class MerchantDetail(APIView):
    def post(self, req):
        from_date = req.data.get('from_date')
        to_date = req.data.get('to_date')
        request_fields = ['from_date', 'to_date']
        validation_response = validate_request_data(request_fields, req.data)
        if not validation_response["status"]:
            return Response(validation_response, status=status.HTTP_400_BAD_REQUEST)
        start_date = datetime.strptime(from_date, '%Y-%m-%d')
        end_date = datetime.strptime(to_date, '%Y-%m-%d')
        if start_date > end_date:
            return Response({"status": False, "message": "from_date must be greater than to to_date"})
        merchant_res = merchant_service.get_merchant_info(start_date, end_date)
        if merchant_res:
            return Response({"Merchant_Info": merchant_res, "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            raise custom_exceptions.DataNotFound("Data Not Found")


class CheckLogin(APIView):
    def post(self, req):
        userLoginId = req.data.get('userLoginId')
        password = req.data.get('password')
        request_fields = ['userLoginId', 'password']
        validation_response = validate_request_data(request_fields, req.data)
        if not validation_response["status"]:
            return Response(validation_response, status=status.HTTP_400_BAD_REQUEST)
        login_response = merchant_service.check_login_data(userLoginId, password)
        if login_response:
            return Response(login_response, status=status.HTTP_200_OK)
        else:
            raise custom_exceptions.DataNotFound("Data Not Found")


class UpdateComment(APIView):
    def post(self, request):
        client_code = request.data.get('client_code')
        comments = request.data.get('comments')
        request_fields = ['client_code', 'comments']
        validation_response = validate_request_data(request_fields, request.data)
        if not validation_response["status"]:
            return Response(validation_response, status=status.HTTP_400_BAD_REQUEST)
        comment_res = merchant_service.update_merchant_comment(client_code, comments)
        return Response({"Message": comment_res, "status": status.HTTP_200_OK})


class CommentSave(APIView):
    def post(self, request):
        request_fields = ['client_code', 'login_id', 'comments', 'merchant_tab']
        validation_response = validate_request_data(request_fields, request.data)
        if not validation_response["status"]:
            return Response(validation_response, status=status.HTTP_400_BAD_REQUEST)
        save_comment = merchant_service.save_comment(request.data)
        return Response({"message": save_comment, "status": True})


class GetComment(APIView):
    def post(self, request):
        client_code = request.data.get('client_code')
        request_fields = ['client_code']
        validation_response = validate_request_data(request_fields, request.data)
        if not validation_response["status"]:
            return Response(validation_response, status=status.HTTP_400_BAD_REQUEST)
        get_comment_data = merchant_service.get_comment_data(client_code)
        if get_comment_data:
            return Response({"Data": get_comment_data, "status": status.HTTP_200_OK})
        else:
            raise custom_exceptions.DataNotFound("Data Not Found")


class RateMapClone(APIView):
    def post(self, req):
        parentClientCode = req.data.get('parentClientCode')
        newClientCode = req.data.get('newClientCode')
        loginId = req.data.get('loginId')
        url = "https://adminapi.sabpaisa.in/SabPaisaAdmin/REST/Ratemapping/cloning/" + str(
            parentClientCode) + "/" + str(newClientCode) + "/" + str(loginId)
        response = requests.get(url) 
        return Response(data=response.json())


class RateMappingGenerateClient(APIView):
    def post(self, req):
        url = 'https://adminapi.sabpaisa.in/SabPaisaAdmin/REST/config/GenerateClientFormForCob'
        x = requests.post(url, json=req.data)
        return Response(x)
