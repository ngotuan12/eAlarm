'''
Created on Aug 15, 2014

@author: TuanNA
'''
from django.db import models
from django.contrib.auth.models import User
from myapp.models.Device import Device

# Create your models here.
class UserDevice(models.Model):
    device = models.ForeignKey(Device,db_column='device_id')
    user = models.ForeignKey(User,db_column='user_id')
    class Meta:
        db_table = 'user_device'
        app_label = 'myapp'