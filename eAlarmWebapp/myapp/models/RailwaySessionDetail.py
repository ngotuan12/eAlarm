'''
Created on Aug 15, 2014

@author: TuanNA
'''
from django.db import models
from myapp.models.DeviceInfor import DeviceInfor
from myapp.models.RailwaySession import RailwaySession

# Create your models here.
class RailwaySessionDetail(models.Model):
    infor = models.ForeignKey(DeviceInfor,db_column='infor_id')
    railway_session = models.ForeignKey(RailwaySession,db_column='r_id')
    value = models.FloatField(db_column='value')
    start_date = models.DateTimeField(db_column='start_date')
    end_date = models.DateTimeField(db_column='end_date')
    issue_date = models.DateTimeField(db_column='issue_date')
    status = models.CharField(max_length=1)
    class Meta:
        db_table = 'railway_session_detail'
        app_label = 'myapp'