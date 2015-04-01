'''
Created on Apr 3, 2014

@author: TuanNA
'''
import json

from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.http.response import HttpResponse
from django.views.decorators.http import require_http_methods

from myapp.models.Device import Device
from myapp.models.DeviceInfor import DeviceInfor
from myapp.models.RailwaySession import RailwaySession
from myapp.util import DateEncoder


@login_required(login_url='/login')
@require_http_methods(["POST",])
def index(request):
	try:
		device_id=request.POST['device_id']
		device = Device.objects.get(id=device_id)
		device_infor= DeviceInfor.objects.filter(device_id=device,status='1').order_by('device_pro__id')
# 		print(device_infor.query)
		infors =[]
		for infor in device_infor:
			infors.append({'id':infor.id,'value':infor.value,'status':infor.status,'properties':model_to_dict(infor.device_pro)})
		route = None
		if device.route is not None:
			route = model_to_dict(device.route)
		return HttpResponse(json.dumps({'device_infor':infors,'device':model_to_dict(device),'route':route}) ,content_type="application/json")
	except Exception as ex:
		return HttpResponse(json.dumps({"error": str(ex)}),content_type="application/json")
@login_required(login_url='/login')
@require_http_methods(["POST",])
def getRaiwayHistory(request):
	try:
		device_id=request.POST['device_id']
		device = Device.objects.get(id=device_id)
		histories= RailwaySession.objects.filter(device = device)
		railway_session = []
		for history in histories:
			railway_session.append(model_to_dict(history))
		return HttpResponse(json.dumps({'railway_session':railway_session},cls = DateEncoder.DateTimeEncoder) ,content_type="application/json")
	except Exception as ex:
		return HttpResponse(json.dumps({"error": str(ex)}),content_type="application/json")
