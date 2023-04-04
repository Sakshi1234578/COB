from rest_framework.views import APIView
from ..DatabaseService.ZoneMasterDetail import zone_master_detail
from rest_framework import status
from rest_framework.response import Response
from ..utils import custom_exceptions


class ZoneMasterDetail(APIView):
    def post(self, req):
        #if not req.data.get('zoneCode'):
        #    raise custom_exceptions.IncompleteDataException("please provide zone code")
        Master_data = zone_master_detail(req.data.get('zoneCode'))
        if Master_data:
            return Response({"zone_master": Master_data, "status": status.HTTP_200_OK},
                            status=status.HTTP_200_OK)
        else:
            raise custom_exceptions.DataNotFound("Data Not Found")
