'''
Created on Aug 15, 2014

@author: TuanNA
'''
import datetime

from django.contrib.auth.models import User
from django.db import models

from myapp.models.Cmd import Cmd
from myapp.models.Device import Device


class DeviceCmdLog(models.Model):
    device = models.ForeignKey(Device,db_column='device_id')
    cmd = models.ForeignKey(Cmd,db_column='cmd_id')
    user = models.ForeignKey(User,db_column='user_id')
    type = models.CharField(max_length=10,db_column='type')
    status = models.CharField(max_length=10,db_column='status')
    content = models.CharField(max_length=500,db_column='content')
    create_date = models.DateTimeField(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),db_column="create_date")
    class Meta:
        db_table = 'device_cmd_log'
        app_label = 'myapp'