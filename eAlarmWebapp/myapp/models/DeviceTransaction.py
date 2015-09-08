'''
Created on Aug 15, 2014

@author: TuanNA
'''
from django.db import models

from myapp.models.Device import Device


# Create your models here.
class DeviceTransaction(models.Model):
    device = models.ForeignKey(Device,db_column='device_id')
    device_status = models.CharField(max_length=1,default ='1')
    start_date = models.DateTimeField(db_column='start_date')
    end_date = models.DateTimeField(db_column='end_date')
    description = models.CharField(max_length=500)
    class Meta:
        db_table = 'device_transaction'
        app_label = 'myapp'