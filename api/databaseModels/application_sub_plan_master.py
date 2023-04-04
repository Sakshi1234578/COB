from django.db import models


class application_sub_plan_master(models.Model):
    plan_id = models.AutoField(primary_key=True)
    plan_code = models.CharField(max_length=5, null=True)
    active = models.BooleanField(default=False)
    plan_description = models.CharField(max_length=255, null=True)
    plan_price = models.CharField(max_length=50, null=True)
    plan_validity_days = models.IntegerField(null=True)
    app_id = models.ForeignKey(
        "api.application_master",
        on_delete=models.CASCADE,
        null=True,
        db_column="app_id",
    )
    plan_name = models.CharField(max_length=100, null=True)
    plan_type = models.CharField(max_length=200, null=True)
    actual_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "application_sub_plan_master"
