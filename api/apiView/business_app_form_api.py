from rest_framework.views import APIView
from api.DatabaseService import business_app_form_service
from rest_framework.response import Response
from ..utils.CodeConstent import codeConstant
from rest_framework import status
from ..utils.Validation import validate_request_data
from datetime import datetime
from api.databaseModels.business_app_form import BusinessAppForm
from api.utils.data import ModifyPage 
from api.Serilizers.business_app_form_serializer import BusinessAppFormSerializer
from django.core.paginator import Paginator
from datetime import datetime , timedelta
from django.db.models import Q
from api.utils.custom_exceptions import InvalidFormatException
import operator
from functools import reduce 




class BusinessAppFormAPI(APIView):
    def post(self, request):
        form_data = request.data 
        request_fields = ['merchant_business_name','merchant_legal_name','merchant_address','product_name','types_of_entity',
    'year_of_establishment','merchant_portal','average_transaction_amount','expected_transactions_numbers','annual_transaction_value','account_details',
    'question','authorized_contact_person_name','authorized_contact_person_email_id','authorized_contact_person_contact_number',
    'technical_contact_person_name','technical_contact_person_email_id','technical_contact_person_contact_number','mcc','nature_of_business',
    'zone','entity_pan_card_number','gst_number'
     ]
        validation_response = validate_request_data(request_fields, form_data)
        if not validation_response["status"]:
            return Response(validation_response, status=status.HTTP_400_BAD_REQUEST)
        response = business_app_form_service.business_app_form_data(form_data)
        if response:
            return Response({"message": codeConstant.user_register.value, "status": status.HTTP_200_OK},
                            status=status.HTTP_200_OK)

# short code:-

    def get(self,request):
        start_date=request.data.get("start_date")
        end_date=request.data.get("end_date")

        q_list=[]
        
        if start_date != None:
                start_date = datetime.strptime(start_date, "%Y-%m-%d")
        else:
                start_date = datetime.min
        if end_date != None:
                end_date = datetime.strptime(end_date, "%Y-%m-%d")
        else:
                end_date = datetime.now()
        q_list.append(Q(created_on__range=[start_date, end_date + timedelta(days=1)]))       
        if start_date > end_date:
                raise InvalidFormatException("start_date cannot be greater than end_date")    
        queryset = BusinessAppForm.objects.filter(reduce(operator.and_, q_list)).order_by("-id") 
        paginator = ModifyPage()
        page = paginator.paginate_queryset(queryset, request)
            
        if page is not None :
            serializer = BusinessAppFormSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
                    
        else:
            serializer = BusinessAppFormSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)   
            
    


# when you want both pagination and without pagination     
      
    #def get(self,request):

    #    start_date=request.data.get('start_date')
    #    end_date=request.data.get('end_date')
        
    #    if start_date and end_date:
    #        start = datetime.strptime(start_date, '%Y-%m-%d')
    #        end = datetime.strptime(end_date, '%Y-%m-%d')
    #        queryset = BusinessAppForm.objects.filter(created_on__range=(start , end + timedelta(days = 1))).order_by("-id")
    #        paginator = ModifyPage()
    #        page = paginator.paginate_queryset(queryset, request)
            
    #        if page is not None :
    #            serializer = BusinessAppFormSerializer(page, many=True)
    #            return paginator.get_paginated_response(serializer.data)
                    
    #        else:
    #            serializer = BusinessAppFormSerializer(queryset, many=True)
    #            return Response(serializer.data, status=status.HTTP_200_OK)
    #    else:
    #        queryset = BusinessAppForm.objects.all()
    #        paginator = ModifyPage()
    #        page = paginator.paginate_queryset(queryset, request)
    #        records=request.query_params.get("records")
            
    #        if page is not None :
    #            serializer = BusinessAppFormSerializer(page, many=True)
    #            return paginator.get_paginated_response(serializer.data)
                    
    #        else:
    #            serializer = BusinessAppFormSerializer(queryset, many=True)
    #            return Response(serializer.data, status=status.HTTP_200_OK)
            
             
# how to fetch particular data from starting and end date
# how to apply pagination 

    #def get(self,request):
    #    start_date=request.data.get('start_date')
    #    end_date=request.data.get('end_date')

    #    if start_date and  end_date:
    #                start = datetime.strptime(start_date, '%Y-%m-%d')
    #                end = datetime.strptime(end_date, '%Y-%m-%d')
    #                if  start_date > end_date:
    #                    return Response("start_date cannot be greater than end_date", status= status.HTTP_400_BAD_REQUEST)
    #                order_by = request.query_params.get("order_by", "id")
    #                queryset = BusinessAppForm.objects.all().order_by(order_by)
    #                paginator = ModifyPage()
    #                serializer = BusinessAppFormSerializer(page, many=True)
    #                page = paginator.paginate_queryset(queryset, request)

    #                if page is not None:
    #                    serializer = BusinessAppFormSerializer(page, many=True)
    #                    return paginator.get_paginated_response(serializer.data)
    #                else:
    #                    serializer = BusinessAppFormSerializer(queryset, many=True)
    #                    return Response(serializer.data)              
    #                response = business_app_form_service.get_data(start, end)
    #                print(response)
    #                return Response(response, status=status.HTTP_200_OK)
    #    else:
    #how to get all the data if startdate and enddate is not given
    #                order_by = request.query_params.get("order_by", "id")
    #                queryset = BusinessAppForm.objects.all().order_by(order_by)
    #                paginator = ModifyPage()
    #                page = paginator.paginate_queryset(queryset, request)
    #                if page is not None:
    #                    serializer = BusinessAppFormSerializer(page, many=True)
    #                    return paginator.get_paginated_response(serializer.data)
    #                else:
    #                    serializer = BusinessAppFormSerializer(queryset, many=True)
    #                    return Response(serializer.data)
    #                data= business_app_form_service.complete_data() 
    #                return Response(data, status=status.HTTP_200_OK)
