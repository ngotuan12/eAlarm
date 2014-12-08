'''
Created on Aug 15, 2014

@author: DienND
'''

from django.db import models

class Department(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    create_date =models.DateField()
    class Meta:
            db_table = 'department'