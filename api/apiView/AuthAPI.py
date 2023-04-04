from rest_framework import status
from ..DatabaseService import AuthService
from ..DatabaseService import OTPService
from ..databaseModels.login_master import login_master
from rest_framework.views import APIView
from rest_framework.response import Response
from ..utils.CodeConstent import codeConstant
from ..Serilizers.OtpSerializer import OtpSerializer
from ..databaseModels.verification import Verification
from ..DatabaseService.AuthService import checkcode
from api.DatabaseService import merchant_service
from ..utils import custom_exceptions
from ..utils.Validation import validate_request_data


class register_api(APIView):
    def post(self, req):
        if req.method == 'POST':
            value = AuthService.register(req.data)
            if value == "User registered":
                return Response({"message": codeConstant.User_registered.value, "status": status.HTTP_200_OK},
                                status=status.HTTP_200_OK)
            else:
                return Response({"message": value, "status": status.HTTP_500_INTERNAL_SERVER_ERROR},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class email_verify(APIView):
    def put(self, request, login_id):
        if request.method == 'PUT':
            try:
                user = login_master.objects.get(loginMasterId=login_id)
                if user is not None:
                    merchant_service.create_merchant_from_login(user)
                if user is None:             
                    return Response(False)
                elif user.status == 'Activate':
                    try:
                        Verification.objects.get(login_id=login_id)
                    except Verification.DoesNotExist:
                        verify_table = Verification()
                        login_data = login_master.objects.get(loginMasterId=login_id)
                        verify_table.login_id = login_data
                        verify_table.save()
                        merchant_service.create_merchant_email_verified(login_id)
                    return Response(False)
                elif user.status == 'Pending' or user.status is None or user.status == '':
                    user.status = 'Activate'
                    user.save()
                    merchant_service.create_merchant_email_verified(login_id)
                    verify_table = Verification()
                    login_data = login_master.objects.get(loginMasterId=login_id)
                    verify_table.login_id = login_data
                    verify_table.save()
                    return Response(True)
            except login_master.DoesNotExist:
                return Response(False)


class login_api(APIView):
    def post(self, req):
        login_response = AuthService.login(req.data)
        if login_response:
            return Response(login_response, status=status.HTTP_200_OK)
        else:
            return Response({"message": login_response, "status": status.HTTP_500_INTERNAL_SERVER_ERROR},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WebsiteLoginAPI(APIView):
    def post(self, req):
        login_id = req.data.get("login_id")
        request_fields = ['login_id']
        validation_response = validate_request_data(request_fields, req.data)
        if not validation_response["status"]:
            return Response(validation_response, status=status.HTTP_400_BAD_REQUEST)
        login_response = AuthService.website_app_and_plan_login(login_id)
        return Response({"data": login_response, "status": status.HTTP_200_OK})


class otp_view(APIView):
    def post(self, req):
        if req.method == 'POST':
            serializer = OtpSerializer(data=req.data)
            if serializer.is_valid():
                otp_data = serializer.validated_data
                response = OTPService.save_otp(otp_data)
                if response == "Email is not correct":
                    raise custom_exceptions.EmailNotCorrect(
                        "Email is not correct")
                return Response(response, status=200 if response['status'] else 400)
            return Response(serializer.errors, status=400)


class validate_otp(APIView):
    def post(self, req):
        response = OTPService.validate_otp(req.data)
        return Response(response, status=200 if response['status'] else 400)


class forgot_password(APIView):
    def put(self, req):
        response = AuthService.forgot_pass(req.data)
        return Response(response, status=200 if response['status'] else 400)


class change_password(APIView):
    def put(self, req):
        response = AuthService.update_password(req.data)
        return Response(response, status=200 if response['status'] else 400)


class check_client_code(APIView):
    def post(self, req):
        res = checkcode(req.data)
        return Response(res, status=200 if res['status'] else 400)
