'''
Created on Dec 3, 2014

@author: TuanNA
'''
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import  Group, User
from django.core.context_processors import csrf
from django.db.models.aggregates import Max
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from myapp.models import Device, Area, DeviceProperties, DeviceInfor, Route
from myapp.models.ApParam import ApParam
from myapp.models.DeviceType import DeviceType


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
        lsSensorDirection = DeviceProperties.objects.filter(p_type='2',m_type='3')
        lsDeviceType = DeviceType.objects.all()
        lsRailwayDirection = ApParam.objects.filter(type='RAILWAY_DIRECTION')
        departments =Group.objects.all()
        routes =Route.objects.all()
        users =User.objects.all().order_by("username")
        context={
                 'lsSensorDirection':lsSensorDirection,'lsArea':lsArea,
                 'lsRailwayDirection':lsRailwayDirection,
                 'lsDeviceType':lsDeviceType,
                 'departments':departments,'users':users,'routes':routes
                 }
        context.update(csrf(request))
    elif request.method == 'POST':
        try:
            _code = request.POST['txtCode'].strip()
            _name = request.POST['txtJourney'].strip()
            _route =request.POST['slRoute'].strip()
            _ManagementUnit =request.POST['slManagementUnit'].strip()
            _UserUnit =request.POST['slUserUnit'].strip()
            _manager =request.POST['txtManager'].strip()
            _phoneNumber =request.POST['txtPhoneNumber'].strip()
            _note =request.POST['txtNote'].strip()
            
            _mac = request.POST['txtMAC'].strip()
            _area_id = request.POST['slArea'].strip()
            _address = request.POST['txtAddress'].strip()
            _fullName = request.POST['txtFullName'].strip()
            _lat = request.POST['txtLat'].strip()
            _lng = request.POST['txtLng'].strip()
            _deviceType = request.POST['slDeviceType'].strip()
            device_type = DeviceType.objects.get(id=_deviceType)
            area = Area.objects.get(id = _area_id)
            group =Group.objects.get(id=_ManagementUnit)
            user =User.objects.get(id=_UserUnit)
            route =Route.objects.get(id=_route)
            
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
            device.owner_name=_manager
            device.owner_phone=_phoneNumber
            device.group= group
            device.user=user
            device.route =route
            device.type ='4'
            _order = Device.objects.filter(route=route).aggregate(Max('order'))['order__max']
            device.order = _order + 1
            device.device_type = device_type
            if _deviceType == '3':
                _railwayDirection = request.POST['slRailwayDirection'].strip()
                _sensorDirection = request.POST['slSensorDirection'].strip()
                sensorDirection = DeviceProperties.objects.get(id = _sensorDirection)
                device.railway_direction = _railwayDirection
                device.sensor_direction = sensorDirection
                device.sensor_direction_code = sensorDirection.code
            device.save()
            #add device infor by device type
            properties = DeviceProperties.objects.filter(device_type = device_type)
            for device_property in properties:
                infor = DeviceInfor()
                infor.device = device
                infor.device_pro = device_property
                infor.value = 0
                infor.status = '1'
                infor.save()
            return HttpResponseRedirect('/railway/list/')
        except Exception as ex:
            print(ex)
            context.update({'has_error':str(ex)})
    return render_to_response("railway/add-railway.html", context, RequestContext(request))
@login_required(login_url='/login')
def edit_railway(request,railway_id):
    lsArea = Area.objects.filter(level = '2')
    departments =Group.objects.all()
    routes =Route.objects.all()
    users =User.objects.all().order_by("username")
    lsSensorDirection = DeviceProperties.objects.filter(p_type='2',m_type='3')
    lsDeviceType = DeviceType.objects.all()
    lsRailwayDirection = ApParam.objects.filter(type='RAILWAY_DIRECTION')
    device = Device.objects.get(id=railway_id)
    current_device_type_id = device.device_type.id
    context={
             'lsSensorDirection':lsSensorDirection,'lsArea':lsArea,
             'lsDeviceType':lsDeviceType,'lsRailwayDirection':lsRailwayDirection,
             'device':device,'departments':departments,'users':users,'routes':routes
             }
    if request.method == 'POST':
        try:
            _code = request.POST['txtCode'].strip()
            _name = request.POST['txtJourney'].strip()
            _route =request.POST['slRoute'].strip()
            _ManagementUnit =request.POST['slManagementUnit'].strip()
            _UserUnit =request.POST['slUserUnit'].strip()
            _manager =request.POST['txtManager'].strip()
            _phoneNumber =request.POST['txtPhoneNumber'].strip()
            _note =request.POST['txtNote'].strip()
            
            _mac = request.POST['txtMAC'].strip()
            _area_id = request.POST['slArea'].strip()
            _address = request.POST['txtAddress'].strip()
            _fullName = request.POST['txtFullName'].strip()
            _lat = request.POST['txtLat'].strip()
            _lng = request.POST['txtLng'].strip()
            _deviceType = request.POST['slDeviceType'].strip()
            device_type = DeviceType.objects.get(id = _deviceType)
            new_device_type_id = device_type.id
            area = Area.objects.get(id = _area_id)
            group =Group.objects.get(id=_ManagementUnit)
            user =User.objects.get(id=_UserUnit)
            route =Route.objects.get(id=_route)
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
            device.owner_name=_manager
            device.owner_phone=_phoneNumber
            device.group= group
            device.user=user
            device.route=route
            device.type ='4'
            device.device_type = device_type
            if _deviceType == '3':
                _railwayDirection = request.POST['slRailwayDirection'].strip()
                _sensorDirection = request.POST['slSensorDirection'].strip()
                sensorDirection = DeviceProperties.objects.get(id = _sensorDirection)
                device.railway_direction = _railwayDirection
                device.sensor_direction = sensorDirection
                device.sensor_direction_code = sensorDirection.code
            device.save()
            if current_device_type_id != new_device_type_id:
                #delete old device infor
                DeviceInfor.objects.filter(device=device).delete()
                #add device infor by device type
                properties = DeviceProperties.objects.filter(device_type = device_type)
                for device_property in properties:
                    infor = DeviceInfor()
                    infor.device = device
                    infor.device_pro = device_property
                    infor.value = 0
                    infor.status = '1'
                    infor.save()
            return HttpResponseRedirect('/railway/list/')
        except Exception as ex:
            print(ex)
            context.update({'has_error':str(ex)})
    context.update(csrf(request))
    return render_to_response("railway/edit-railway.html", context, RequestContext(request))
@login_required(login_url='/login')
def delete_railway(request,railway_id):
    device = Device.objects.get(id=railway_id)
    deviceInfos = DeviceInfor.objects.filter(device =str(device.id))
    for di in deviceInfos:
        di.delete()
    device.delete()
    return HttpResponseRedirect('/railway/list/')