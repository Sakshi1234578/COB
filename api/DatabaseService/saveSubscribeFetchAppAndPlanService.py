from ..Serilizers.clientSubscribedPlanDetailsSerializer import clientSubscribedPlanDetailsSerializer
import traceback
from ..DatabaseService import email_service
from api.config.config import Configuration
from ..databaseModels.client_subscribed_plan_details import client_subscribed_plan_details
from datetime import timedelta
from ..databaseModels.login_master import login_master
from datetime import date
import uuid


def saveSubscribeFetchAppAndPlan(data):
    serializer = clientSubscribedPlanDetailsSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    validate_client_email(data)
    return "Data saved successfully"


def validate_client_email(data):
    try:
        email_url = Configuration.get_Property("cob_dashboard")
        client_data = get_client_id(data.get('clientId'))
        email_service.validate_subscribed_and_plan_email(client_data.email, client_data.name, email_url)
        email_service.validate_subscribed_and_plan_internal_mail("rahmat786@gmail.com",
                                                                 "enterprise-product-detail", "Rahmat Ali",
                                                                 data.get('planName'), data.get("applicationName"),
                                                                 client_data.name, client_data.mobileNumber,
                                                                 str(date.today()))

    except Exception as e:
        traceback.print_exc()


def get_client_id(client_id):
    try:
        print("Getting client", client_id)
        client_data = login_master.objects.get(master_client_id=client_id)
        print("Getting client", client_data)
        return client_data
    except Exception as e:
        traceback.print_exc()


def GetSubscibedPlanDetail(startDate, endDate, client_ID):
    if client_ID == "":
        subscribedData = client_subscribed_plan_details.objects.filter(
            mandateStartTime__range=(startDate, endDate + timedelta(days=1)))
    else:
        subscribedData = client_subscribed_plan_details.objects.filter(
            mandateStartTime__range=(startDate, endDate + timedelta(days=1)), clientId=client_ID)
    data = clientSubscribedPlanDetailsSerializer(subscribedData, many=True).data
    res = []
    for i in range(len(data)):
        loginData = get_client_id(data[i]['clientId'])
        if loginData.isDirect:
            res.append(data[i])
    return res


def pre_update_client_subscribed_plan_detail(
    clientSubscribedPlanDetailsId,appId,planId,clientCode,clientName,clientId,purchaseAmount):
        try:
            get_client_subscribe_id=client_subscribed_plan_details.objects.get(clientSubscribedPlanDetailsId=clientSubscribedPlanDetailsId)
        except Exception:
            traceback.print_exc()
            return "Client subscribed Id Not Found" 
        get_client_subscribe_id.clientTxnId = uuid.uuid4()
        get_client_id.client_subscribed_plan_details=client_subscribed_plan_details
        get_client_subscribe_id.appId= appId
        get_client_subscribe_id.planId = planId
        get_client_subscribe_id.clientCode=clientCode
        get_client_subscribe_id.clientName=clientName
        get_client_subscribe_id.clientId=clientId
        get_client_subscribe_id.purchaseAmount=purchaseAmount   
        get_client_subscribe_id.save()

        data_response={
            "clientTxnId":get_client_subscribe_id.clientTxnId 
        }
        return data_response