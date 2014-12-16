'''
Created on Aug 15, 2014

@author: TuanNA
'''
from myapp.models.Area import Area
from myapp.models.Route import Route
from django.contrib.auth.models import  Group,User
from django.db import models

# Create your models here.
class Device(models.Model):
    code = models.CharField(max_length=10)
    area = models.ForeignKey(Area,db_column='area_id')
    name = models.CharField(max_length=100)
    lat = models.FloatField()
    lng = models.FloatField()
    address = models.CharField(max_length=200)
    mac_add = models.CharField(max_length=30)
    short_address = models.CharField(max_length=200)
    connected_server = models.CharField(max_length=30)
    status = models.CharField(max_length=1,default ='0')
    type = models.CharField(max_length=1,default ='1')
    description = models.CharField(max_length=500,db_column="description")
    next = models.ForeignKey('self',db_column='next_id',null=True)
    user=models.ForeignKey(User,db_column='user_id')
    group=models.ForeignKey(Group,db_column='group_id')
    owner_name=models.CharField(max_length=100)
    owner_phone=models.CharField(max_length=25)
    route = models.ForeignKey(Route,db_column='route_id',null=True)
    class Meta:
        db_table = 'device'
        app_label = 'myapp'
        permissions = (
            ("view_device", "Can see list device"),
        )