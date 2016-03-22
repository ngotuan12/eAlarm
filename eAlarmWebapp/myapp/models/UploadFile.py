'''
Created on Aug 15, 2014

@author: DienND
'''
from django.db import models

# Create your models here.
class UploadFile(models.Model):
    type = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    dir = models.CharField(max_length=200)
    class Meta:
        db_table = 'upload_file'
        app_label = 'myapp'
        permissions = (
        )