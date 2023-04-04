from django.db import models


class comment_master(models.Model):
    id = models.AutoField(primary_key=True)
    comments = models.TextField(null=True, db_column='comments')
    comment_by = models.ForeignKey('api.login_master', on_delete=models.CASCADE, null=True, db_column='comment_by')
    comment_on = models.DateTimeField(null=False, blank=False, auto_now=True, db_column='comment_on')
    comment_type = models.CharField(max_length=100, null=True, db_column='comment_type')
    client_code = models.CharField(max_length=100, null=True, db_column='client_code')
    merchant_tab = models.CharField(max_length=100, null=True, db_column='merchant_tab')
    file_name = models.CharField(max_length=100, null=True)
    file_path = models.CharField(max_length=255, null=True, db_column='file_Path')

    class Meta:
        db_table = 'comment_master'
