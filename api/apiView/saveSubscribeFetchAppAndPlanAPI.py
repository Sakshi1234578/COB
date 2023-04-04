from rest_framework.views import APIView
from ..DatabaseService.saveSubscribeFetchAppAndPlanService import saveSubscribeFetchAppAndPlan
from api.databaseModels.client_application_mapper import client_application_mapper
from ..databaseModels.client_subscribed_plan_details import client_subscribed_plan_details
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from ..databaseModels.client_super_master import client_super_master
from ..databaseModels.lookup_application import lookup_application
from ..utils import custom_exceptions
from ..Serilizers.clientSubscribedPlanDetails import clientSubscribedPlanDetailsSerializer
from ..Serilizers.clientSubscribedPlanDetails import clientSubscribedPlanDetailsSerializer
from datetime import datetime
from ..DatabaseService.saveSubscribeFetchAppAndPlanService import GetSubscibedPlanDetail
from ..utils.Validation import validate_request_data, validate_request_data_empty_string

from ..DatabaseService.saveSubscribeFetchAppAndPlanService import pre_update_client_subscribed_plan_detail


class clientSubscribedPlan(APIView):
    def post(self, req):
        if req.method == 'POST':
            client_id = req.data.get('clientId')
            application_id = req.data.get('applicationId')
            if client_subscribed_plan_details.objects.filter(Q(clientId=client_id), Q(applicationId=application_id)).exists():
                raise custom_exceptions.SubscriptionAlreadyExist("Client has already subscribed please choose another plan")


            # ================== On Hold ========================
            # if client_application_mapper.objects.filter(clientId=client_id, application_id=application_id).exists():
            #     raise custom_exceptions.SubscriptionAlreadyExist("Client has already subscribed please choose another "
            #                                                      "plan")
            # client_application = client_application_mapper()
            # client_application.clientId = client_super_master.objects.get(clientId=client_id)
            # client_application.application_id = lookup_application.objects.get(applicationId=application_id)
            # client_application.status = "Verified"
            # client_application.subscriptionStatus = "Subscribed"
            # client_application.reason = "NA"
            # client_application.save()


            subscribedData = saveSubscribeFetchAppAndPlan(req.data)
            if subscribedData == "Data saved successfully":
                return Response({"message": subscribedData, "status": status.HTTP_200_OK},
                                status=status.HTTP_200_OK)
            else:
                return Response({"message": subscribedData, "status": status.HTTP_400_BAD_REQUEST},
                                status=status.HTTP_400_BAD_REQUEST)


class GetSubscribedPlanDetailByClientId(APIView):
    def post(self, req):
        try:
            subscribedData = client_subscribed_plan_details.objects.filter(Q(clientId=req.data.get('clientId')),
                                                                           Q(applicationId=req.data.get(
                                                                               'applicationId'))).first()
            data = clientSubscribedPlanDetailsSerializer(subscribedData)
            return Response({"data": data.data, "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": e, "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)

class GetSubscribedPlanDetailsByDate(APIView):
    def post(self, req):
        request_fields = ['from_date', 'to_date']
        validation_response = validate_request_data(request_fields, req.data)
        if not validation_response["status"]:
            return Response(validation_response, status=status.HTTP_400_BAD_REQUEST)
        empty_request_fields = ['client_ID']
        validation_response = validate_request_data_empty_string(empty_request_fields, req.data)
        if not validation_response["status"]:
            return Response(validation_response, status=status.HTTP_400_BAD_REQUEST)
        from_date = req.data.get('from_date')
        to_date = req.data.get('to_date')
        client_ID = req.data.get('client_ID')
        start_date = datetime.strptime(from_date, '%Y-%m-%d')
        end_date = datetime.strptime(to_date, '%Y-%m-%d')
        SubscribedDetail = GetSubscibedPlanDetail(start_date, end_date, client_ID)
        return Response(SubscribedDetail)


class PreUpdateSubscribedPlanDetail(APIView):
    def put(self,req):
        clientSubscribedPlanDetailsId=req.data.get("clientSubscribedPlanDetailsId")
        appId=req.data.get("appId")
        planId=req.data.get("planId")
        clientCode=req.data.get("clientCode")
        clientName=req.data.get("clientName")
        #print(clientName)
        clientId=req.data.get("clientId")
        purchaseAmount=req.data.get("purchaseAmount")
        request_fields=['clientSubscribedPlanDetailsId','appId','planId','clientCode','clientName','clientId','purchaseAmount']
        validation_response=validate_request_data(request_fields, req.data)
        if  not validation_response["status"]:
            return Response(validation_response, status=status.HTTP_400_BAD_REQUEST)
        data_update= pre_update_client_subscribed_plan_detail(clientSubscribedPlanDetailsId,
        appId,planId,clientCode,clientName,clientId,purchaseAmount)
        return Response({"message": data_update, "status": status.HTTP_200_OK},
                        status=status.HTTP_200_OK)
