'''
Created on Dec 3, 2014

@author: TuanNA
'''
import json

from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
#from django.core.context_processors import csrf

from myapp.models import DeviceProperties
from myapp.models.Device import Device
from myapp.models.DeviceInfor import DeviceInfor
from myapp.util.DateEncoder import DateEncoder
from myapp.models.ApParam import ApParam

@login_required(login_url='/login')
def index(request):
    #devices = DeviceProperties.objects.filter(p_type='2')
    devices =  DeviceProperties.objects.raw("SELECT `id`, `code`, `name`, `description`, `type`, `min`, `max`, `min_alarm`, `max_alarm`, `symbol`, `require`, `parent_id`, `p_type`, `on_railway`, `m_type` m_type_id,(select `par_name` from `ap_param` where `par_type`='M_TYPE' and `par_value`=d.`m_type`) m_type_name FROM `device_properties` d WHERE `p_type`='2' ")
    mtypes = ApParam.objects.filter(type='M_TYPE')
    
    context={'devices':devices,'mtypes':mtypes}
    return render_to_response("railway/property.html", context, RequestContext(request))
@login_required(login_url='/login')
def add_property(request):
    context={}
    mtypes = ApParam.objects.filter(type='M_TYPE')
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
            _mtypeid = request.POST['slMType']
            m_type = mtypes.get(value=_mtypeid,type='M_TYPE')
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
            dp.m_type = m_type.value
            
            if request.POST.get('cbRequire') :
                dp.require = '0'
                _parent_id =request.POST['slParent']
            else:
                dp.require = '1'
                
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
    mtypes = ApParam.objects.filter(type='M_TYPE')
    #curr_dp = DeviceProperties.objects.filter(id=property_id)
    #context={'curr_dp':curr_dp}
    #context={'property_id':"axxxxxxxxxxxxxxxx"}
    context={}
    if request.method == 'POST':
        try:
            _code = request.POST['txtCodeEdit']
            _name = request.POST['txtNameEdit']
            _description = request.POST['txtDescriptionEdit']
            _type = request.POST['slTypeEdit']
            if str(_type) =='2':
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
            _mtypeid = request.POST['slMTypeEdit']
            #m_type = mtypes.get(value=_mtypeid,type='M_TYPE')
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
            #dp.m_type = m_type.value
            dp.m_type = _mtypeid
            
            if request.POST.get('cbRequireEdit') :
                dp.require = '0'
                _parent_id =request.POST['slParentEdit']
            else:
                dp.require = '1'
            dp.parent_id = _parent_id
            dp.save()
            return HttpResponseRedirect('/railway/property/')
        except Exception as ex:
            print(ex)
#    context.update(csrf(request))
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