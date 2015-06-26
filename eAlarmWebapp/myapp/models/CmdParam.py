from django.db import models

from myapp.models.Cmd import Cmd


class CmdParam(models.Model):
    cmd = models.ForeignKey(Cmd,db_column='cmd_id')
    parent = models.ForeignKey('self',db_column='parent_id')
    status = models.CharField(max_length=1)
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=50)
    type = models.CharField(max_length=1)
    class Meta:
        db_table = 'cmd_param'
        app_label = 'myapp'