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
            ("view_device_report", "Xem báo cáo tổng hợp trạng thái phòng máy"),
            ("view_device_detail_report", "Xem báo cáo tổng hợp chi tiết hoạt động phòng máy"),
            ("view_device_error_report", "Xem báo cáo thống kê lỗi phòng máy"),
        )