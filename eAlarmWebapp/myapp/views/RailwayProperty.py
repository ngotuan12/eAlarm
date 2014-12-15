'''
Created on Dec 3, 2014

@author: TuanNA
'''
import json

from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from myapp.models import DeviceProperties
from myapp.models.Device import Device
from myapp.models.DeviceInfor import DeviceInfor
from myapp.util.DateEncoder import DateEncoder


@login_required(login_url='/login')
def index(request):
    devices = DeviceProperties.objects.filter(p_type='2')
    context={'devices':devices}
    return render_to_response("railway/property.html", context, RequestContext(request))
@login_required(login_url='/login')
def add_property(request):
    context={}
    if request.method == 'POST':
        try:
            _code = request.POST['txtCode']
            _name = request.POST['txtName']
            _type = request.POST['slType']
            _description = request.POST['txtDescription']
            if str(_type) =='1':
                _min = float(request.POST['txtMin'])
                _max = float(request.POST['txtMax'])
                _minAlarm = float(request.POST['txtMinAlarm'])
                _maxAlarm = float(request.POST['txtMaxAlarm'])
                _symbol = request.POST['txtSymbol']
            else:
                _min = float('0')
                _max = float('0')
                _minAlarm = float('0')
                _maxAlarm = float('0')
                _symbol = ''
            _parent_id = None
            p_type ='2'
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
            dp.p_type = p_type
            
            if request.POST.get('cbRequire1') :
                dp.require = '0'
            else :
                dp.require = '1'
            if request.POST.get('cbRequire') :
                _parent_id =request.POST['slParent']
            
            dp.parent_id = _parent_id
            dp.save()
            
            lsDevice = Device.objects.filter(type='4')
            for device in lsDevice :
                deviceInfo = DeviceInfor()
                
                deviceInfo.device = device
                deviceInfo.device_pro = dp
                deviceInfo.status = '0'
                deviceInfo.value = float('0')
                
                deviceInfo.save()
            return HttpResponseRedirect('/railway/property/')
        except Exception as ex:
            print(ex)
    return render_to_response("railway/add-device-property.html", context, RequestContext(request))
@login_required(login_url='/login')
def edit_property(request,property_id):
    context={}
    if request.method == 'POST':
        try:
            _code = request.POST['txtCodeEdit']
            _name = request.POST['txtNameEdit']
            _description = request.POST['txtDescriptionEdit']
            _type = request.POST['slTypeEdit']
            if str(_type) =='1':
                _min = float(request.POST['txtMinEdit'])
                _max = float(request.POST['txtMaxEdit'])
                _minAlarm = float(request.POST['txtMinAlarmEdit'])
                _maxAlarm = float(request.POST['txtMaxAlarmEdit'])
                _symbol = request.POST['txtSymbolEdit']
            else:
                _min = float('0')
                _max = float('0')
                _minAlarm = float('0')
                _maxAlarm = float('0')
                _symbol = ''
            _parent_id = None
            p_type ='2'
            
            dp = DeviceProperties.objects.get(id=property_id,p_type='2')
            dp.code = _code
            dp.name = _name
            dp.type = _type
            dp.description = _description
            dp.min = _min 
            dp.max = _max
            dp.min_alarm = _minAlarm
            dp.max_alarm = _maxAlarm
            dp.symbol = _symbol
            dp.p_type = p_type
            
            if request.POST.get('cbRequireEdit1') :
                dp.require = '0'
            else :
                dp.require = '1'
                
            if request.POST.get('cbRequireEdit') :
                _parent_id =request.POST['slParentEdit']
            dp.parent_id = _parent_id
            dp.save()
            return HttpResponseRedirect('/railway/property/')
        except Exception as ex:
            print(ex)
    return render_to_response("railway/edit-device-property.html", context, RequestContext(request))
@login_required(login_url='/login')
def delete_property(request,property_id):
    dp = DeviceProperties.objects.get(id=property_id)
    deviceInfos = DeviceInfor.objects.filter(device_pro =str(dp.id))
    for di in deviceInfos:
        di.delete()
    dp.delete()
    return HttpResponseRedirect('/railway/property/')
def get_property(request,p_id,p_code):
    try:
        if p_id== 'no_id':
            properties = DeviceProperties.objects.filter(p_type='2',code=p_code)
        else:
            properties = DeviceProperties.objects.exclude(id=p_id).filter(p_type='2',code=p_code)
        value='0'
        if len(properties) >0 :
            value ='1'
        return HttpResponse(json.dumps({'property':value},cls=DateEncoder) ,content_type="application/json")
    except Exception as ex:
        return HttpResponse(json.dumps({"error": str(ex)}),content_type="application/json")