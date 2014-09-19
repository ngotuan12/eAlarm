'''
Created on Apr 3, 2014

@author: TuanNA
'''
# @login_required(login_url='/signin')
from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from myapp.models import Device
from myapp.models.Area import Area
from myapp.util import client
from myapp.models.DeviceProperties import DeviceProperties


@login_required(login_url='/login')
@permission_required('myapp.view_device_report',login_url='/permission-error')
def view_device_report(request):
	context = {'devices':Device.objects.all().order_by("code","name","address"),'areas':Area.objects.filter(status="1").order_by("woodenleg","code")}
	if(request.POST) :
		device_id = request.POST["slDevice"]
		area_id = request.POST["slArea"]
		device_status = request.POST["slStatus"]
		authorization = client.getAuthorization()
		fileOut = client.exportDeviceReport(authorization,device_id,area_id,device_status)
		return HttpResponseRedirect('/report/'+fileOut)
	context.update(csrf(request))
	return render_to_response("report/device-report.html", context,RequestContext(request))
@login_required(login_url='/login')
@permission_required('myapp.view_device_detail_report',login_url='/permission-error')
def view_device_detail_report(request):
	context = {'devices':Device.objects.all().order_by("code","name","address"),'areas':Area.objects.filter(status="1").order_by("woodenleg","code")}
	if(request.POST) :
		device_id = request.POST["slDevice"]
		area_id = request.POST["slArea"]
		device_status = request.POST["slStatus"]
		from_date = request.POST["dtFromDate"]
		to_date = request.POST["dtToDate"]
		authorization = client.getAuthorization()
		fileOut = client.exportDeviceDetailReport(authorization,device_id,area_id,device_status,from_date,to_date)
		return HttpResponseRedirect('/report/'+fileOut)
	context.update(csrf(request))
	return render_to_response("report/device-detail-report.html", context,RequestContext(request))
@login_required(login_url='/login')
@permission_required('myapp.view_device_error_report',login_url='/permission-error')
def view_device_error_report(request):
	context = {'devices':Device.objects.all().order_by("code","name","address"),'areas':Area.objects.filter(status="1").order_by("woodenleg","code")}
	context.update({'properties':DeviceProperties.objects.filter(require='1')})
	if(request.POST) :
		device_id = request.POST["slDevice"]
		area_id = request.POST["slArea"]
		device_status = request.POST["slStatus"]
		property_id = request.POST["slProperty"]
		from_date = request.POST["dtFromDate"]
		to_date = request.POST["dtToDate"]
		authorization = client.getAuthorization()
		fileOut = client.exportDeviceErrorReport(authorization,device_id,area_id,device_status,property_id,from_date,to_date)
		return HttpResponseRedirect('/report/'+fileOut)
	context.update(csrf(request))
	return render_to_response("report/device-error-report.html", context,RequestContext(request))
@login_required(login_url='/login')
@permission_required('myapp.view_sensor_mirror_report',login_url='/permission-error')
def view_sensor_mirror_report(request):
	context = {'devices':Device.objects.all().order_by("code","name","address"),'areas':Area.objects.filter(status="1").order_by("woodenleg","code")}
	context.update({'properties':DeviceProperties.objects.filter(require='0')})
	if(request.POST) :
		device_id = request.POST["slDevice"]
		area_id = request.POST["slArea"]
		device_status = request.POST["slStatus"]
		property_id = request.POST["slProperty"]
		from_date = request.POST["dtFromDate"]
		to_date = request.POST["dtToDate"]
		authorization = client.getAuthorization()
		fileOut = client.exportSensorMirrorReport(authorization,device_id,area_id,device_status,property_id,from_date,to_date)
		return HttpResponseRedirect('/report/'+fileOut)
	context.update(csrf(request))
	return render_to_response("report/sensor-mirror-report.html", context,RequestContext(request))