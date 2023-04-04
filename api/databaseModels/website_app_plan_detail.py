from django.db import models
from api.databaseModels.login_master import login_master


class WebsiteAppPlanDetail(models.Model):
    id = models.AutoField(primary_key=True)
    login_id = models.ForeignKey(login_master, on_delete=models.CASCADE, null=False, db_column="login_id")
    plan_details = models.JSONField(null=True, blank=True)
    created_date = models.DateTimeField(null=False, blank=False, auto_now_add=True)

    class Meta:
        db_table = "website_app_plan_detail"
