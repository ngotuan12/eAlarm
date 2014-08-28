# -*- coding: utf8 -*-
'''
Created on Aug 15, 2014

@author: TuanNA
'''
from django.db import models

class Report(models.Model):
    class Meta:
        app_label = 'myapp'
        permissions = (
            ("view_device_report", "Xem báo cáo tổng hợp phòng máy"),
            ("view_device_detail_report", "Xem báo cáo tổng hợp chi tiết phòng máy"),
        )