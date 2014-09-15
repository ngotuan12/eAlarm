'''
Created on Apr 3, 2014

@author: DienND
'''

from django.contrib.auth.decorators import permission_required
from django.core.context_processors import csrf
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response

from myapp.models import DeviceProperties,DeviceInfor


@permission_required('myapp.change_deviceproperties',login_url='/permission-error')
def index(request):
	if request.method == 'GET':
		lsDeviceProperty = DeviceProperties.objects.all()
		context={'lsDeviceProperty':lsDeviceProperty}
		context.update(csrf(request))
		return render_to_response("device-property.html", context)
	elif request.method == 'POST':
		formType= request.POST['type']
		if formType == 'editDeviceProperty':
			
			_id = request.POST['hd_device_property_id']
			_code = request.POST['txtCode']
			_name = request.POST['txtName']
			_type = request.POST['slType']
			_description = request.POST['txtDescription']
			_min = float(request.POST['txtMin'])
			_max = float(request.POST['txtMax'])
			_minAlarm = float(request.POST['txtMinAlarm'])
			_maxAlarm = float(request.POST['txtMaxAlarm'])
			_symbol = request.POST['txtSymbol']
			
			dp = DeviceProperties.objects.get(id = _id)
			
			dp.code = _code
			dp.name = _name
			dp.type = _type 
			dp.description = _description
			dp.min = _min 
			dp.max = _max
			dp.min_alarm = _minAlarm
			dp.max_alarm = _maxAlarm
			dp.symbol = _symbol
			if request.POST.get('cbRequire1') :
				dp.require = '1'
			else :
				dp.require = '0'
				
			dp.save()
			
			return HttpResponseRedirect('/device-property')
		elif formType == 'deleteDeviceProperty':
			_id = request.POST['hd_device_pro']
			dp = DeviceProperties.objects.get(id = _id)
			
			slDeviceInfo = DeviceInfor.objects.filter(device_pro = _id)
			for deviceInfo in slDeviceInfo :
				deviceInfo.delete()
				
			dp.delete()
			return HttpResponseRedirect('/device-property')