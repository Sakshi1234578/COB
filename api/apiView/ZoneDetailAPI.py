
from rest_framework.views import APIView
from ..DatabaseService.zoneService import zone_detail
from rest_framework import status
from rest_framework.response import Response



class ZoneDetails(APIView):
    def get(self, req):
        try:
            category_data = zone_detail()
            if category_data:
                return Response({"zones": category_data, "status": status.HTTP_200_OK},
                                status=status.HTTP_200_OK) 
        except Exception as e:
            return Response({"error": e, "status": status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


