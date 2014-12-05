'''
Created on Dec 3, 2014

@author: TuanNA
'''
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from myapp.models import Device, Area, DeviceProperties, DeviceInfor


@login_required(login_url='/login')
def index(request):
    devices = Device.objects.filter(type='4')
    context={'devices':devices}
    return render_to_response("railway/list.html", context, RequestContext(request))
@login_required(login_url='/login')
def add_railway(request):
    context={}
    if request.method == 'GET':
        lsArea = Area.objects.filter(level = '2')
        lsProperty = DeviceProperties.objects.all()
        context={'lsArea':lsArea,'lsProperty':lsProperty}
        context.update(csrf(request))
    elif request.method == 'POST':
        try:
            _code = request.POST['txtRoute'].strip()
            _name = request.POST['txtJourney'].strip()
            _ManagementUnit =request.POST['slManagementUnit'].strip()
            _manager =request.POST['txtManager'].strip()
            _phoneNumber =request.POST['txtPhoneNumber'].strip()
            _note =request.POST['txtNote'].strip()
            
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
            device.description = _note
            device.type ='4'
            device.save()
 
 
#             lsDeviceProperties = DeviceProperties.objects.all()
#             for deviceProperties in lsDeviceProperties:
#                 temp = deviceProperties
#                 deviceInfor = DeviceInfor()
#                 deviceInfor.device = device
#                 deviceInfor.value = float('0')
#                 if request.POST.get(str(temp.code)):
#                     deviceInfor.status = '1'
#                 else :
#                     deviceInfor.status = '0'
#                      
#                 deviceInfor.device_pro = temp
#                 deviceInfor.save()
                 
            return HttpResponseRedirect('/railway/list/')
        except Exception as ex:
            print(ex)
    return render_to_response("railway/add-railway.html", context, RequestContext(request))
@login_required(login_url='/login')
def edit_railway(request,railway_id):
    lsArea = Area.objects.filter(level = '2')
    lsProperty = DeviceProperties.objects.all()
    device = Device.objects.get(id=railway_id)
    context={'lsArea':lsArea,'lsProperty':lsProperty,'device':device}
    if request.method == 'POST':
        try:
            _code = request.POST['txtRoute'].strip()
            _name = request.POST['txtJourney'].strip()
            _ManagementUnit =request.POST['slManagementUnit'].strip()
            _manager =request.POST['txtManager'].strip()
            _phoneNumber =request.POST['txtPhoneNumber'].strip()
            _note =request.POST['txtNote'].strip()
            
            _mac = request.POST['txtMAC'].strip()
            _area_id = request.POST['slArea'].strip()
            _address = request.POST['txtAddress'].strip()
            _fullName = request.POST['txtFullName'].strip()
            _lat = request.POST['txtLat'].strip()
            _lng = request.POST['txtLng'].strip()
            area = Area.objects.get(id = _area_id)
    #                 
            device.name = _name
            device.address = _fullName
            device.short_address = _address
            device.mac_add = _mac
            device.area = area
            device.code = _code
            device.lat = float(_lat)
            device.lng = float(_lng)
            device.description = _note
            device.type ='4'
            device.save()
            return HttpResponseRedirect('/railway/list/')
        
        except Exception as ex:
            print(ex)
    context.update(csrf(request))
    return render_to_response("railway/edit-railway.html", context, RequestContext(request))
@login_required(login_url='/login')
def delete_railway(request,railway_id):
    device = Device.objects.get(id=railway_id)
    device.delete()
    return HttpResponseRedirect('/railway/list/')