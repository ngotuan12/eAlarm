'''
Created on Aug 15, 2014

@author: TuanNA
'''
from django.db import models
from myapp.models.Device import Device
# Create your models here.
class LastAction(models.Model):
    device_id = models.ForeignKey(Device,db_column='device_id')
    type = models.CharField(max_length=15)
    start_date = models.DateField()
    end_date = models.DateField()
    data = models.CharField(max_length=200)
    class Meta:
        db_table = 'last_action'
        app_label = 'myapp'
