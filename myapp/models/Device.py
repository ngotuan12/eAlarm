'''
Created on Aug 15, 2014

@author: TuanNA
'''
# from myapp.models.Area import Area
from django.db import models

# Create your models here.
class Device(models.Model):
    code = models.CharField(max_length=10)
#     area_id = models.ForeignKey(Area)
    name = models.CharField(max_length=100)
    lat = models.FloatField()
    lng = models.FloatField()
    address = models.CharField(max_length=200)
    mac_add = models.CharField(max_length=30)
    short_address = models.CharField(max_length=200)
    connected_server = models.CharField(max_length=30)
    status = models.CharField(max_length=1)
    class Meta:
        db_table = 'device'