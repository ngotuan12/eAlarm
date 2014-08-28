# -*- coding: utf8 -*-
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

from myapp.models import Area,Device,DeviceProperties,DeviceInfor

@login_required(login_url='/login')
@permission_required('myapp.change_device',login_url='/permission-error')
def index(request):
	if request.method == 'GET':
		try:
			_device_id = request.GET['device_id']
			device = Device.objects.get(id = _device_id)
			lsArea = Area.objects.filter(level = '2')
			lsInfor = DeviceInfor.objects.filter(device = _device_id)
			lsProperty = DeviceProperties.objects.all()
			context={'lsInfor':lsInfor,'device':device,'lsArea':lsArea,'lsProperty':lsProperty}
			context.update(csrf(request))
		except Exception as ex:
			context={}
			print(ex)
		finally:
			return render_to_response("edit-device.html", context,RequestContext(request))
	elif request.method == 'POST':
		formType= request.POST['type']
		if formType == "editDevice":
			context={}
			try:
				_device_id = request.POST['txtDeviceId'].strip()
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
				device = Device.objects.get(id = _device_id)
				
				device.name = _name
				device.address = _fullName
				device.short_address = _address
				device.mac_add = _mac
				device.area = area
				device.code = _code
				device.lat = float(_lat)
				device.lng = float(_lng)
				device.save()


				lsDeviceInfor = DeviceInfor.objects.filter(device = _device_id)
				
				for deviceInfor in lsDeviceInfor:
					temp = deviceInfor
					deviceProperty = DeviceProperties.objects.get(id = temp.device_pro_id)
					if request.POST.get(str(deviceProperty.code)):
						temp.status = '1'
					else :
						temp.status = '0'
					temp.save()
					
				return HttpResponseRedirect('/device-list')
			except Exception as ex:
				print(ex)
		elif formType == "deleteDevice":
			_device_id = request.POST['hd_device_id'].strip()
			device = Device.objects.get(id = _device_id)
			lsDeviceInfor = DeviceInfor.objects.filter(device = _device_id)
			
			for deviceInfor in lsDeviceInfor:
				deviceInfor.delete()
				
			device.delete()
			
			return HttpResponseRedirect('/device-list')