from ..Serilizers.ProductCatalogue import product_catalogue_serializer
from ..Serilizers.ProductSubCatalogue import product_subdetails_serializer
from ..databaseModels.application_master import application_master
from ..databaseModels.application_sub_plan_master import application_sub_plan_master


def  Product_details():
    productData = application_master.objects.filter(active=1)
    if(len(productData)==0):
        return "No Product"
    return product_catalogue_serializer(productData, many=True).data

def product_sub_details(app_id):
    productData = application_sub_plan_master.objects.filter(app_id=app_id, active=1)
    if(len(productData)==0):
        return "No Product"
    return product_subdetails_serializer(productData, many=True).data