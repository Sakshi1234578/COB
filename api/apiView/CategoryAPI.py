from rest_framework.views import APIView
from ..DatabaseService import category_service
from rest_framework.response import Response
from rest_framework import status
from ..utils.Validation import validate_request_data


class category_api(APIView):
    def get(self, req):
        if req.method == 'GET':
            category_data = category_service.category_details()
            if category_data:
                return Response({"message": category_data, "status": status.HTTP_200_OK},
                                status=status.HTTP_200_OK)
            else:
                return Response({"message": category_data, "status": status.HTTP_500_INTERNAL_SERVER_ERROR},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RiskBusinessCategoryMapper(APIView):
    def post(self, req):
        risk_category_code = req.data.get('risk_category_code')
        request_fields = ['risk_category_code']
        validation_response = validate_request_data(request_fields, req.data)
        if not validation_response["status"]:
            return Response(validation_response, status=status.HTTP_400_BAD_REQUEST)
        category_mapper_service = category_service.get_category_business_id_mapper(risk_category_code)
        return Response({"Data": category_mapper_service, "status": status.HTTP_200_OK},
                        status=status.HTTP_200_OK)
