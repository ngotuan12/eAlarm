'''
Created on Aug 15, 2014

@author: TuanNA
'''
import datetime

from django.db import models


# Create your models here.
class Route(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    order = models.IntegerField(max_length=11)
    create_date = models.DateTimeField(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),db_column="create_date")
    class Meta:
        db_table = 'route'
        app_label = 'myapp'
        permissions = (
            ("view_route", "Can see list route"),
        )