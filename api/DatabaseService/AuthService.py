from ..databaseModels.login_master import login_master
from ..Serilizers.registrationSerializer import registration_loginserializer, website_login_serializer
from .LoginResponse import login_response
from ..databaseModels.OTP import OTP
from api.databaseModels.rate_template_master import RateTemplateMaster
from ..databaseModels.client_super_master import client_super_master
from ..utils import custom_exceptions
from api.config.config import Configuration
from ..DatabaseService import email_service
from api.DatabaseService import merchant_service
from ..utils import Validation
from api.databaseModels.website_app_plan_detail import WebsiteAppPlanDetail
from rest_framework.response import Response

email_url = Configuration.get_Property("EMAIL_VERIFICATION_URL")


def register(data):
    email = data.get("email")
    user = login_master.objects.filter(email=email).first()
    check_email_id = check_email_format(email)
    if check_email_id is False:
        raise custom_exceptions.EmailIDNotCorrect("check your email")
    if user:
        raise custom_exceptions.EmailAlreadyExist("email_id already exists")
    if login_master.objects.filter(mobileNumber=data.get("mobileNumber")).exists():
        raise custom_exceptions.MobileNumberAlreadyExist("mobile number already exist")
    if (not data.get("isDirect")) and (not data.get("requestId") or data.get("requestId") == ""):
        raise custom_exceptions.BlankData("Please send the requestId")
    if data["requestedClientType"] == 1:
        data["requestedClientType"] = "Individual"
    elif data["requestedClientType"] == 2:
        data["requestedClientType"] = "Bussiness"
    else:
        raise custom_exceptions.ClientTypeNotCorrect("client type is not correct")
    if data.get("roleId") is None:
        data["roleId"] = 4
    data["username"] = email
    serializer = registration_loginserializer(data=data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        login_id = serializer.data["loginMasterId"]
        to = serializer.data["email"]
        user_name = serializer.data["username"]
        name = serializer.data["name"]
        msg = f"{email_url}{login_id}"
        # This condition is only for production
        # if data.get('isDirect'):
        #     URL = "https://sabpaisa.targetcrm.in/LeadsAPI.php"
        #     email = serializer.data['email']
        #     mobile = serializer.data['mobileNumber']
        #     payload= f'_operation=InsertLead&name={name}&email={email}&mobile={mobile}&leadsource=Website Organic'
        #     headers = {
        #             'Content-Type': 'application/x-www-form-urlencoded'
        #         }
        #     response = requests.request("POST", URL, headers=headers, data=payload)
        #     print(response.text)
        if data.get('plan_details'):
            create_or_update_website_app_plan_detail(login_id, data.get('plan_details'))
        email_service.validate_email(to, name, user_name, msg)
        return "User registered"
    return "User Registered"


def check_email_format(email_id):
    url = Configuration.get_Property("CHECK_EMAIL_URL")
    payload = {"email_id": email_id}
    headers = {'api-key': Configuration.get_Property('CHECK_EMAIL_API_KEY')}
    response = Validation.send_request(url, payload, headers, "POST")
    res = response.json()
    print("Email id Response", response.json())
    if res.get('is_validated'):
        return True
    else:
        return False


def login(data):
    #username = data.get("clientUserId")
    #password = data.get("userPassword")
    #if username is None or username == "" or password is None or password == "":
    #    raise custom_exceptions.BlankData("Username or password is blank or none")
    user = login_master.objects.filter(username=username).first()
    if not user:
        raise custom_exceptions.UserNotExistException("user not exist")
    elif user.password != password:
        raise custom_exceptions.PassNotExistException("password is incorrect")
    elif user.status == "Pending" or user.status is None or user.status == "":
        to = user.email
        name = user.name
        user_name = user.username
        login_id = user.loginMasterId
        msg = f"{email_url}{login_id}"
        email_service.validate_email(to, name, user_name, msg)
        raise custom_exceptions.VerifyUserFirst("EmailId Is Not Verified")
    elif user.status == "Activate":
        data = login_response(username, password)
        return data


def website_app_and_plan_login(login_id):
    get_website_res = get_website_res = get_website_data(login_id)
    if not get_website_res:
        raise custom_exceptions.DataNotFound("Data Not Found")
    return website_login_serializer(get_website_res, many=True).data


def forgot_pass(data):
    try:
        if not data.get("email") or not data.get("verification_token") or not data.get("password"):
            return {"status": False, "message": "Please provide all the data"}
        otp_response = OTP.objects.get(
            verification_token=data.get("verification_token"))
        if otp_response.is_expired:
            return {"status": False, "message": "otp is expired"}
        if otp_response.status == "Pending":
            return {"status": False, "message": "verify your otp"}
        login_data = login_master.objects.get(email=otp_response.email)
        login_data.password = data.get("password")
        login_data.save()
        return {"status": True, "message": "Password changed!"}
    except (OTP.DoesNotExist, login_master.DoesNotExist):
        return {"status": False, "message": "Invalid Data"}
    except Exception:
        return {"status": False, "message": "Server Error"}


def update_password(data):
    try:
        if not data.get("email") or not data.get("password") or not data.get("newpassword"):
            return {"status": False, "message": "Please provide all the data"}
        login_data = login_master.objects.get(email=data.get("email"))
        if login_data.password != data.get("password"):
            return {
                "status": False,
                "message": "The old password you have entered is incorrect",
            }
        login_data.password = data.get("newpassword")
        login_data.save()
        return {"status": True, "message": "password update successfully"}
    except login_master.DoesNotExist:
        return {"status": False, "message": "Invalid password"}
    except Exception:
        return {"status": False, "message": "server Error"}


def checkcode(data):
    client_code = data.get("client_code")
    if client_code is not None and client_code != "" and len(client_code)!=0:
        for data in client_code:
            print(">>>>>", data)
            if not client_super_master.objects.filter(clientCode=data).exists(): 
                return { "clientCode": data,"status":True , "message":"client code is unique" }
        return {"status":False , "message":"client code is not unique" }
    return  {"status":False , "message":"Please send client code list" }
           
    

def create_or_update_website_app_plan_detail(login_id, plan_details):
    try:
        website_data = WebsiteAppPlanDetail.objects.get(login_id=login_id)
    except Exception:
        website_data = WebsiteAppPlanDetail()
    website_data.plan_details = plan_details
    website_data.login_id = merchant_service.check_login_master_id(login_id)
    website_data.save()


def get_website_data(login_id):
    try:
        return WebsiteAppPlanDetail.objects.filter(login_id=login_id)
    except Exception:
        return None
