from rest_framework.views import APIView
from ..DatabaseService.Product_catalogue_service import Product_details
from ..DatabaseService.Product_catalogue_service import product_sub_details
from rest_framework.response import Response
from rest_framework import status


class Product_catalogue(APIView):
    def get(self, req):
        if req.method == 'GET':
            productData = Product_details()
            if productData == "No Product":
                return Response({"ProductDetail": productData, "status": status.HTTP_400_BAD_REQUEST},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"ProductDetail": productData, "status": status.HTTP_200_OK},
                                status=status.HTTP_200_OK)


class Product_catalogue_subdetail(APIView):
    def get(self, req, app_id):
        if req.method == 'GET':
            product_sub_data = product_sub_details(app_id)
        if product_sub_data == "No Product":
            return Response({"ProductDetail": product_sub_data, "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"ProductDetail": product_sub_data, "status": status.HTTP_200_OK},
                            status=status.HTTP_200_OK)
