'''
Created on Aug 15, 2014

@author: DienND
'''
from django.db import models

# Create your models here.
class ApParam(models.Model):
    type = models.CharField(max_length=15,db_column='par_type')
    name = models.CharField(max_length=15,db_column='par_name')
    value = models.CharField(max_length=100,db_column='par_value')
    desc = models.CharField(max_length=200,db_column='description') 
    class Meta:
        db_table = 'ap_param'
        app_label = 'myapp'
        permissions = (
            ("view_ap_param", "Can see list ap_param"),
        )