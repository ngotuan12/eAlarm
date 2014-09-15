'''
Created on Apr 3, 2014

@author: DienND
'''

from django.contrib.auth.decorators import permission_required
from django.core.context_processors import csrf
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from myapp.models import DeviceProperties,Device,DeviceInfor


@permission_required('myapp.add_deviceproperties',login_url='/permission-error')
def index(request):
	if request.method == 'GET':
		lsDeviceProperty = DeviceProperties.objects.all()
		context={'lsDeviceProperty':lsDeviceProperty}
		context.update(csrf(request))
		return render_to_response("device-property.html", context,RequestContext(request))
	elif request.method == 'POST':
		formType= request.POST['type']
		if formType == 'addDeviceProperty':
			
			_code = request.POST['txtCode']
			_name = request.POST['txtName']
			_type = request.POST['slType']
			_description = request.POST['txtDescription']
			_min = float(request.POST['txtMin'])
			_max = float(request.POST['txtMax'])
			_minAlarm = float(request.POST['txtMinAlarm'])
			_maxAlarm = float(request.POST['txtMaxAlarm'])
			_symbol = request.POST['txtSymbol']
			
			dp = DeviceProperties()
			dp.code = _code
			dp.name = _name
			dp.type = _type 
			dp.description = _description
			dp.min = _min 
			dp.max = _max
			dp.min_alarm = _minAlarm
			dp.max_alarm = _maxAlarm
			dp.symbol = _symbol
			
			if request.POST.get('cbRequire') :
				dp.require = '1'
			else :
				dp.require = '0'
			dp.save()
			
			lsDevice = Device.objects.all()
			for device in lsDevice :
				deviceInfo = DeviceInfor()
				
				deviceInfo.device = device
				deviceInfo.device_pro = dp
				deviceInfo.status = '0'
				deviceInfo.value = float('0')
				
				deviceInfo.save()
			
			return HttpResponseRedirect('/device-property')
		elif formType == 'editDeviceProperty':
			print('edit')
			return HttpResponseRedirect('/device-property')