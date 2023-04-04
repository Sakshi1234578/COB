from rest_framework.views import APIView
from ..DatabaseService.EmployeeMasterService import employeeMaster
from rest_framework import status
from rest_framework.response import Response
from ..utils import custom_exceptions


class employeeMasterDetail(APIView):
    def post(self, req):
        if not req.data.get('ManagerId'):
           raise custom_exceptions.IncompleteDataException("please provide ManagerId")
        employee_data = employeeMaster(req.data.get('ManagerId'))
        if employee_data:
            return Response({"zone_master": employee_data, "status": status.HTTP_200_OK},
                            status=status.HTTP_200_OK)
        else:
            return Response({"error": employee_data, "status": status.HTTP_404_NOT_FOUND},
                            status=status.HTTP_404_NOT_FOUND)
