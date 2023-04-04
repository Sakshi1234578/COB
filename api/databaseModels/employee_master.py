from django.db import models


class employee_master(models.Model):
    id = models.AutoField(primary_key=True)
    empName = models.CharField(max_length=45, null=True, db_column='emp_name')
    empCode = models.CharField(max_length=45, null=True, db_column='emp_code')
    emp_email = models.CharField(max_length=100, null=True, db_column='emp_email')
    empContactNumber = models.CharField(max_length=45, null=True, db_column='emp_contact_number')
    isActive = models.BooleanField(default=True, db_column='is_active')
    managerId = models.CharField(max_length=20, null=True, db_column='manager_id')
    roleCode = models.CharField(max_length=20, null=True, db_column='role_code')
    deptCode = models.CharField(max_length=20, null=True, db_column='dept_code')
    designationCode = models.CharField(max_length=45, null=True, db_column='designation_code')
    created_on = models.DateTimeField(null=True, db_column='created_on')
    password = models.CharField(max_length=255, null=True, db_column='password')

    class Meta:
        db_table = 'employee_master'
