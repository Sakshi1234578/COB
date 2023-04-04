from ..Serilizers.ZoneMasterDetails import zoneMasterSerializer
from ..databaseModels.zone_head_master import zone_head_master


def zone_master_detail(zoneCode):
    try:
        zone_master_data = zone_head_master.objects.filter(zoneCode=zoneCode, isActive=True)
        return zoneMasterSerializer(
            zone_master_data, many=True).data
    except Exception as e:
        print(e)


def get_zone_head_name(emp_code):
    try:
        return zone_head_master.objects.filter(empCode=emp_code, isActive=True).values_list('zoneHeadName')
    except Exception as e:
        print(e)
        return None
