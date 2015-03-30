'''
Created on Aug 15, 2014

@author: TuanNA
'''
from django.db import models
from myapp.models.Device import Device

# Create your models here.
class RailwaySession(models.Model):
    device = models.ForeignKey(Device,db_column='device_id')
    start_date = models.DateTimeField(db_column='start_date')
    end_date = models.DateTimeField(db_column='end_date')
    status = models.CharField(max_length=1)
    class Meta:
        db_table = 'railway_session'
        app_label = 'myapp'