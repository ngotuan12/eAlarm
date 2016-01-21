'''
Created on Aug 15, 2014

@author: DienND
'''
from django.db import models
from myapp.models.DeviceProperties import DeviceProperties
from myapp.models.DeviceType import DeviceType

# Create your models here.
class DeviceTypeProperty(models.Model):
    device_type =  models.ForeignKey(DeviceType,db_column='device_type_id')
    property = models.ForeignKey(DeviceProperties,db_column='device_property_id')
    class Meta:
        db_table = 'device_type_property'
        app_label = 'myapp'
        permissions = (
        )