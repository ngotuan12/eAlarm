# -*- coding: utf8 -*-
'''
Created on Apr 3, 2014

@author: TuanNA
'''
from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from myapp.models import Area,DeviceProperties,Device,DeviceInfor


@login_required(login_url='/login')
@permission_required('myapp.add_area',login_url='/permission-error')
def index(request):
	if request.method == 'GET':
		try:
			lsArea = Area.objects.filter(level = '2')
			lsProperty = DeviceProperties.objects.all()
			context={'lsArea':lsArea,'lsProperty':lsProperty}
			context.update(csrf(request))
		except Exception as ex:
			context={}
			print(ex)
		finally:
			return render_to_response("add-device.html", context,RequestContext(request))
	elif request.method == 'POST':
		formType= request.POST['type']
		if formType == "addDevice":
			context={}
			try:
				_code = request.POST['txtCode'].strip()
				_name = request.POST['txtName'].strip()
				_mac = request.POST['txtMAC'].strip()
				_area_id = request.POST['slArea'].strip()
				_address = request.POST['txtAddress'].strip()
				_fullName = request.POST['txtFullName'].strip()
				_lat = request.POST['txtLat'].strip()
				_lng = request.POST['txtLng'].strip()
				area = Area.objects.get(id = _area_id)
# 				
				device = Device()
				
				device.name = _name
				device.address = _fullName
				device.short_address = _address
				device.mac_add = _mac
				device.area = area
				device.code = _code
				device.lat = float(_lat)
				device.lng = float(_lng)
				device.save()


				lsDeviceProperties = DeviceProperties.objects.all()
				for deviceProperties in lsDeviceProperties:
					temp = deviceProperties
					deviceInfor = DeviceInfor()
					deviceInfor.device = device
					deviceInfor.value = float('0')
					if request.POST.get(str(temp.code)):
						deviceInfor.status = '1'
					else :
						deviceInfor.status = '0'
						
					deviceInfor.device_pro = temp
					deviceInfor.save()
					
				return HttpResponseRedirect('/device-list')
			except Exception as ex:
				print(ex)
