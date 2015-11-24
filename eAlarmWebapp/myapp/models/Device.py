'''
Created on Aug 15, 2014

@author: TuanNA
'''
import datetime

from django.contrib.auth.models import  Group, User
from django.db import models

from myapp.models.Area import Area
from myapp.models.Route import Route


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
    action_status = models.CharField(db_column='action_status',max_length=25)
    order = models.IntegerField(max_length=11,default=0)
    create_date = models.DateTimeField(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),db_column="create_date")
    class Meta:
        db_table = 'device'
        app_label = 'myapp'
        permissions = (
            ("view_device", "Can see list device"),
        )
        ordering = ('route__order', 'order')