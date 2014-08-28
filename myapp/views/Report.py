'''
Created on Apr 3, 2014

@author: TuanNA
'''
# @login_required(login_url='/signin')
from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from myapp.models import Device
from myapp.models.Area import Area

@login_required(login_url='/login')
@permission_required('myapp.view_device_report',login_url='/permission-error')
def view_device_report(request):
	context = {'devices':Device.objects.all().order_by("code","name","address"),'areas':Area.objects.filter(status="1").order_by("woodenleg","code")}
	
	context.update(csrf(request))
	return render_to_response("report/device-report.html", context,RequestContext(request))