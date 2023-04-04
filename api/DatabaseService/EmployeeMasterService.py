from ..Serilizers.EmployeeMasterSerializer import employeeMasterSerializer
from ..databaseModels.employee_master import employee_master


def employeeMaster(managerId):
    try:
        employee_master_data = employee_master.objects.filter(managerId=managerId, isActive=True)
        return employeeMasterSerializer(employee_master_data, many=True).data
    except Exception as e:
        print(e)
        return None


def get_emp_name(emp_code):
    try:
        return employee_master.objects.filter(empCode=emp_code, isActive=True).values_list('empName')
    except Exception as e:
        print(e)
        return None
