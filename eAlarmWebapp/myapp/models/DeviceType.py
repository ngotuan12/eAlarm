'''
Created on Aug 15, 2014

@author: DienND
'''
from django.db import models

# Create your models here.
class DeviceType(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    class Meta:
        db_table = 'device_type'
        app_label = 'myapp'
        permissions = (
        )