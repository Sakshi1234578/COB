import traceback
from api.databaseModels.login_master import login_master
from api.databaseModels.merchant_data import merchant_data
from api.databaseModels.rate_template_master import RateTemplateMaster
from api.Serilizers.merchant_serializer import RateTemplateMasterSerializer
from datetime import datetime, timedelta
from ..databaseModels.employee_master import employee_master
from ..utils import custom_exceptions
from api.databaseModels.lookup_business_category import business_category
from api.databaseModels.merchant_data import merchant_data
from api.databaseModels.comment_master import comment_master
from api.databaseModels.merchant_address import merchant_address
from api.databaseModels.zone_master import zone_master
from api.DatabaseService import merchant_document_service
from api.config.config import Configuration
from api.utils.aws_bucket import S3BucketService
from django.db import transaction


def merchant_by_login_id(loginMasterId):
    return merchant_data.objects.get(loginMasterId=loginMasterId)


def create_merchant_email_verified(loginMasterId):
    merch_data = merchant_by_login_id(loginMasterId)
    merch_data.isEmailVerified = True
    merch_data.save()


def create_merchant_from_login(user: login_master):
    try:
        merchant = merchant_by_login_id(user.loginMasterId)
    except Exception:
        merchant = merchant_data()
    merchant.loginMasterId = user
    merchant.name = user.name
    merchant.emilId = user.email
    merchant.contactNumber = user.mobileNumber
    merchant.save()


def get_merchant_info(start_date, end_date):
    try:
        get_login_data = list(login_master.objects.filter(
            isDirect=True, createdDate__range=(start_date, end_date + timedelta(days=1))).values('loginMasterId',
                                                                                                 'name', 'email',
                                                                                                 'mobileNumber',
                                                                                                 'createdDate',
                                                                                                 'status',
                                                                                                 'business_cat_code').order_by(
            '-loginMasterId'))
        try:
            for i in range(len(get_login_data)):
                business_category_set = get_login_data[i]['business_cat_code']
                if business_category_set is None:
                    get_login_data[i]['business_category_name'] = "None"
                    continue
                get_business_cat_name = business_category.objects.filter(category_id=business_category_set).values()
                merchantData =merchant_data.objects.filter(loginMasterId=get_login_data[i]['loginMasterId']).values()
                get_login_data[i]['business_category_name'] = get_business_cat_name[0]['category_name']
                if len(merchantData) != 0:
                    get_login_data[i]['company_name'] = merchantData[0]['companyName']
                    get_login_data[i]['businessType'] = merchantData[0]['businessType']
                    get_login_data[i]['gstNumber'] = merchantData[0]['gstNumber']
                    get_login_data[i]['expectedTransactions'] = merchantData[0]['expectedTransactions']
                    get_login_data[i]['companyWebsite'] = merchantData[0]['companyWebsite']
                    if merchantData[0]['zone_code'] != None:
                        zoneDetail = zone_master.objects.filter(zoneCode=merchantData[0]['zone_code']).values()
                        get_login_data[i]['zone_code'] = zoneDetail[0]['zoneName']
                    else:
                        get_login_data[i]['zone_code'] = 'None'
                else:
                    get_login_data[i]['company_name'] = 'None'
                    get_login_data[i]['businessType'] = 'None'
                    get_login_data[i]['gstNumber'] = 'None'
                    get_login_data[i]['expectedTransactions'] = 'None'
                    get_login_data[i]['companyWebsite'] = 'None'
                    get_login_data[i]['zone_code'] = 'None'
                merchantAddress = merchant_address.objects.filter(login_id=get_login_data[i]['loginMasterId']).values()
                if len(merchantAddress) != 0:
                    get_login_data[i]['address'] = merchantAddress[0]['address'] + merchantAddress[0]['city'] + \
                                                   merchantAddress[0]['state']
                else:
                    get_login_data[i]['address'] = 'None'
        except Exception as err:
            pass
        return get_login_data
    except Exception:
        traceback.print_exc()
        return "No Data Found"


def get_rate_template_data(risk_cat_code):
    try:
        rate_template_data = RateTemplateMaster.objects.filter(risk_cat_code=risk_cat_code, is_active=True)
        return RateTemplateMasterSerializer(rate_template_data, many=True).data
    except Exception:
        traceback.print_exc()
        return "No Data Found"


def get_template_data_by_business_code(business_cat_code):
    try:
        rate_template_data = RateTemplateMaster.objects.filter(business_cat_code=business_cat_code, is_active=True)
        return RateTemplateMasterSerializer(rate_template_data, many=True).data
    except Exception:
        traceback.print_exc()
        return "No Data Found"


def check_login_data(user_email, user_pass):
    user = check_employee_email(user_email)
    if not user:
        raise custom_exceptions.UserNotExistException("User Not Exist")
    elif user.password != user_pass:
        raise custom_exceptions.PassNotExistException("Password is Incorrect")
    get_login_info = employee_master.objects.filter(emp_email=user_email, password=user_pass).values_list(
        "id", "emp_email", "created_on", "isActive", "roleCode", "deptCode")
    if get_login_info[0][3]:
        return_status = "Active"
    else:
        return_status = "NotActive"
    login_response = { 
        "loginId": get_login_info[0][0],
        "userLoginId": get_login_info[0][1], 
        "creationDate": get_login_info[0][2],
        "status": return_status,
        "roleId": get_login_info[0][4],
        "deptId": get_login_info[0][5],
        "companyId": None,
        "password": None
    }
    return login_response


def check_employee_email(email_id):
    return employee_master.objects.filter(emp_email=email_id).first()


def get_risk_template_data_by_code(rate_template_code, business_cat_code, risk_cat_code):
    try:
        template_data = RateTemplateMaster.objects.filter(rate_template_code=rate_template_code,
                                                          business_cat_code=business_cat_code,
                                                          risk_cat_code=risk_cat_code,
                                                          is_active=True)
        return RateTemplateMasterSerializer(template_data, many=True).data
    except Exception:
        traceback.print_exc()
        return "No Data Found"


def update_merchant_comment(client_code, comments):
    try:
        get_client_code = merchant_data.objects.get(clientCode=client_code)
    except Exception:
        traceback.print_exc()
        return "Client Code Not Found"
    get_client_code.comments = comments
    get_client_code.save()
    return "Comment Updated"


def save_comment(merchant_comment):
    check_login_master_id(merchant_comment.get('login_id'))
    check_client_code(merchant_comment.get('client_code'))
    try:
        comment_data = comment_master()
        comment_data.comment_by = check_login_master_id(merchant_comment.get('login_id'))
        comment_data.client_code = merchant_comment.get('client_code')
        comment_data.comments = merchant_comment.get('comments')
        comment_data.merchant_tab = merchant_comment.get('merchant_tab')
        if merchant_comment.get('files'):
            validation_response = merchant_document_service.validate_kyc_doc(merchant_comment.get('files'))
            if not validation_response['status']:
                return validation_response
            doc_folder = Configuration.get_Property("MERCHANT_DOC_FOLDER_COMMENTS")
            file_path = doc_folder + "/MERCHANT_COMMENTS/MERCHANT_" + str(merchant_comment.get('login_id'))
            file_name = merchant_document_service.generate_doc_name(merchant_comment.get('files'))
            comment_data.file_name = file_name
            bucket = S3BucketService()
            file_url = bucket.upload_file(merchant_comment.get('files'), file_path, file_name)
            comment_data.file_path = file_url
        comment_data.save()
        return "Comment Save Successfully"
    except Exception:
        traceback.print_exc()
        return None


def get_comment_data(client_code):
    try:
        comment_data = list(comment_master.objects.filter(client_code=client_code).values(
            'id', 'comments', 'comment_by', 'comment_on', 'comment_type', 'client_code', 'merchant_tab', 'file_name',
            'file_path').order_by('id'))
        for i in range(len(comment_data)):
            get_login_name = login_master.objects.filter(loginMasterId=comment_data[i]['comment_by']).values_list(
                'name')
            comment_data[i]['comment_by_user_name'] = get_login_name[0][0]
        return comment_data
    except Exception:
        traceback.print_exc()
        return None


def check_login_master_id(login_id):
    try:
        return login_master.objects.get(loginMasterId=login_id)
    except login_master.DoesNotExist:
        raise custom_exceptions.DataNotFound("User not found for the given login id")


def check_client_code(client_code):
    try:
        return merchant_data.objects.get(clientCode=client_code)
    except merchant_data.DoesNotExist:
        raise custom_exceptions.DataNotFound("client not found for the given client_code")
