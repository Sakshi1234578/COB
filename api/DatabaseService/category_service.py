import traceback
from ..Serilizers.LookupSerializers import lookup_category_serializer
from ..databaseModels.lookup_category import lookup_category
from ..databaseModels.risk_business_category_mapper import risk_business_category_mapper
from ..databaseModels.risk_category_master import risk_category_master
from ..databaseModels.lookup_business_category import business_category


def category_details():
    get_all_category_data = lookup_category.objects.filter(is_active = 1)
    return lookup_category_serializer(get_all_category_data, many=True).data


def get_category_name(risk_catg_code):
    try:
        return risk_category_master.objects.filter(risk_category_code=risk_catg_code, is_active=True).values_list(
            'risk_category_name')
    except Exception:
        traceback.print_exc()
        return None


def get_category_business_id_mapper(risk_category_code):
    try:
        get_risk_mapper_date = list(
            risk_business_category_mapper.objects.filter(risk_category=risk_category_code).values(
                'risk_category', 'business_category_id'))
        get_business_cat_name = []
        for i in range(len(get_risk_mapper_date)):
            get_business_cat_name = business_category.objects.filter(
                category_id=get_risk_mapper_date[i]['business_category_id']).values_list('category_name')
            get_risk_mapper_date[i]['category_name'] = get_business_cat_name[0][0]
        return get_risk_mapper_date

    except Exception:
        traceback.print_exc()
        return None
