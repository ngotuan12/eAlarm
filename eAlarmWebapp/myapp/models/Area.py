'''
Created on Aug 15, 2014

@author: DienND
'''
from django.db import models

# Create your models here.
class Area(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
#     parent_id = models.ForeignKey('Area',blank=True, null=True, related_name='considered_best_friend_for')
    parent = models.ForeignKey('self',db_column='parent_id')
    level = models.CharField(max_length=5)
    status = models.CharField(max_length=1)
    woodenleg = models.CharField(max_length=50)
    lat = models.FloatField()
    lng = models.FloatField()
    type = models.CharField(max_length=10)
    full_name = models.CharField(max_length=300)
    area_code = models.CharField(max_length=25)
    class Meta:
        db_table = 'area'
        app_label = 'myapp'
        permissions = (
            ("view_area", "Can see list area"),
        )