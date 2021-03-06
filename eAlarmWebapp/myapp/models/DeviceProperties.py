'''
Created on Aug 15, 2014

@author: TuanNA
'''
from django.db import models

from myapp.models.DeviceType import DeviceType


# Create your models here.
class DeviceProperties(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    type = models.CharField(max_length=1)
    min = models.FloatField()
    max = models.FloatField()
    min_alarm = models.FloatField()
    max_alarm = models.FloatField()
    symbol = models.CharField(max_length=15)
    require = models.CharField(max_length=1)
    p_type = models.CharField(max_length=1,default ='1')
    parent = models.ForeignKey('self',db_column='parent_id',null=True)
    on_railway = models.CharField(max_length=1,default ='0')
    device_type = models.ForeignKey(DeviceType,db_column='device_type_id')
    #m_type = models.ForeignKey(ApParam,db_column='m_type',null=True,on_delete=models.SET_NULL)
    m_type = models.CharField(max_length=10)
    class Meta:
        db_table = 'device_properties'
        app_label = 'myapp'
        permissions = (
            ("view_deviceproperties", "Can see list device properties"),
        )
