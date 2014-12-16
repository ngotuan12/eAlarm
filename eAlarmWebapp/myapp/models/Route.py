'''
Created on Aug 15, 2014

@author: TuanNA
'''
from django.db import models

# Create your models here.
class Route(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    class Meta:
        db_table = 'route'
        app_label = 'myapp'
        permissions = (
            ("view_route", "Can see list route"),
        )