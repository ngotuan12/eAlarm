'''
Created on Apr 3, 2014

@author: TuanNA
'''
from datetime import datetime
import json

from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.http.response import HttpResponse
from django.views.decorators.http import require_http_methods

from myapp.models.Device import Device
from myapp.models.DeviceInfor import DeviceInfor
from myapp.models.DeviceTransaction import DeviceTransaction
from myapp.models.RailwaySession import RailwaySession
from myapp.models.RailwaySessionDetail import RailwaySessionDetail
from myapp.util import DateEncoder


@login_required(login_url='/login')
@require_http_methods(["POST", ])
def index(request):
	try:
		device_id = request.POST['device_id']
		device = Device.objects.get(id=device_id)
		device_infor = DeviceInfor.objects.filter(device_id=device, status='1').order_by('device_pro__name')
# 		print(device_infor.query)
		infors = []
		last_railway = {}
		if device.action_status == '0':
			last_railway = RailwaySession.objects.filter(device_id=device_id)
			if len(last_railway)>0:
				last_railway = model_to_dict(last_railway.latest('end_date'))
			else:
				last_railway = []
		for infor in device_infor:
			infors.append({'id':infor.id, 'value':infor.value, 'status':infor.status, 'properties':model_to_dict(infor.device_pro)})
		route = None
		if device.route is not None:
			route = model_to_dict(device.route)
		return HttpResponse(
						json.dumps(
								{
								'device_infor':infors,
								'device':model_to_dict(device),
								'route':route,
								'last_railway':last_railway}
								, cls=DateEncoder.DateTimeEncoder) 
						, content_type="application/json")
	except Exception as ex:
		return HttpResponse(json.dumps({"error": str(ex)}), content_type="application/json")
@login_required(login_url='/login')
@require_http_methods(["POST", ])
def getRaiwayHistory(request):
	try:
		device_id = request.POST['device_id']
		device = Device.objects.get(id=device_id)
		histories = RailwaySession.objects.filter(device=device).order_by('-start_date')
		railway_sessions = []
		for history in histories:
			railway_sessions.append(model_to_dict(history))
		return HttpResponse(json.dumps({'railway_sessions':railway_sessions}, cls=DateEncoder.DateTimeEncoder) , content_type="application/json")
	except Exception as ex:
		return HttpResponse(json.dumps({"error": str(ex)}), content_type="application/json")
@login_required(login_url='/login')
@require_http_methods(["POST", ])
def getRaiwayDetailHistory(request):
	try:
		session_id = request.POST['railway_session_id']
		session = RailwaySession.objects.get(id=session_id)
		details = RailwaySessionDetail.objects.filter(railway_session=session).order_by('infor__device_pro__code')
		railway_detail_sessions = []
		for detail in details:
			railway_detail_sessions.append({'detail':model_to_dict(detail), 'property':model_to_dict(detail.infor.device_pro)})
# 			railway_detail_sessions.append({'infor':detail.infor,'value':detail.value,'status':detail.status,'start_date':detail.start_date})			
		return HttpResponse(json.dumps({'railway_detail_sessions':railway_detail_sessions}, cls=DateEncoder.DateTimeEncoder) , content_type="application/json")
	except Exception as ex:
		return HttpResponse(json.dumps({"error": str(ex)}), content_type="application/json")
@login_required(login_url='/login')
@require_http_methods(["POST", ])
def getDeviceHistory(request):
	try:
		device_id = request.POST['device_id']
		p_from_date = request.POST['from_date']
		p_to_date = request.POST['to_date']
		from_date = datetime.strptime(p_from_date, '%d/%m/%Y')
		to_date = datetime.strptime(p_to_date, '%d/%m/%Y')
		device = Device.objects.get(id=device_id)
		rows = DeviceTransaction.objects.filter(device=device,device_status='2',start_date__gte = from_date,end_date__lte = to_date).order_by('-start_date')
		histories = []
		for row in rows:
			temp = model_to_dict(row)
			if row.end_date is not None and row.start_date is not None:
				temp.update({'time':(row.end_date-row.start_date).seconds})
			else:
				temp.update({'time':'--'})
			histories.append(temp)
		return HttpResponse(json.dumps({'histories':histories}, cls=DateEncoder.DateTimeEncoder) , content_type="application/json")
	except Exception as ex:
		return HttpResponse(json.dumps({"error": str(ex)}), content_type="application/json")
