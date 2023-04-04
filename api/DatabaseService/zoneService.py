from ..Serilizers.zoneDetailSerializer import zoneDetailSerializer
from ..databaseModels.zone_master import zone_master


def zone_detail():
    try:
        zone_master_data = zone_master.objects.filter(isActive=True)
        return zoneDetailSerializer(zone_master_data, many=True).data
    except Exception as e:
        print(e)


def get_zone_name(zone_code):
    try:
        return zone_master.objects.filter(zoneCode=zone_code, isActive=True).values_list('zoneName')
    except Exception as e:
        print(e)
        return None
