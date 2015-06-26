'''
Created on Aug 15, 2014

@author: DienND
'''
from django.db import models

# Create your models here.
class Cmd(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)
    type = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    content = models.CharField(max_length=500)
    class Meta:
        db_table = 'cmd'
        app_label = 'myapp'