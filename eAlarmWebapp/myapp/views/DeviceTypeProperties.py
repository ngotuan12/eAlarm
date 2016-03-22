'''
Created on Dec 3, 2014

@author: TuanNA
'''
import json

from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.decorators.http import require_http_methods

from myapp.models.DeviceType import DeviceType
from myapp.models.DeviceProperties import DeviceProperties
from django.forms.models import model_to_dict
from myapp.models.Device import Device
from myapp.models.DeviceInfor import DeviceInfor


@login_required(login_url='/login')
def index(request):
    types = DeviceType.objects.all()
    context={'types':types}
    return render_to_response("device/device-type-properties.html", context, RequestContext(request))
@login_required(login_url='/login')
@require_http_methods(["POST", ])
def property_list(request):
    try:
        device_type_id = request.POST['device_type_id']
        lsProperties = DeviceProperties.objects.filter(device_type_id=device_type_id,p_type='2').order_by('code')
        properties = []
        for pty in lsProperties:
            properties.append(model_to_dict(pty))
        return HttpResponse(json.dumps({'handle':'success','properties':properties}) , content_type="application/json")
    except Exception as ex:
        return HttpResponse(json.dumps({'handle':'error',"msg": str(ex)}), content_type="application/json")
@login_required(login_url='/login')
@require_http_methods(["POST", ])
def add(request):
    try:
        device_type_id = request.POST['device_type_id']
        device_type = DeviceType.objects.get(id = device_type_id)
        device_property = DeviceProperties()
        device_property.device_type = device_type
        device_property.code = request.POST['code']
        device_property.name = request.POST['name']
        device_property.min = request.POST['min']
        device_property.max = request.POST['max']
        device_property.min_alarm  = request.POST['min_alarm']
        device_property.max_alarm = request.POST['max_alarm']
        device_property.symbol = request.POST['symbol']
        device_property.type = request.POST['type']
        device_property.m_type = request.POST['m_type']
        device_property.p_type = '2'
        device_property.save()
        # Add device infor
        devices = Device.objects.filter(device_type=device_type)
        for device in devices:
            infor = DeviceInfor()
            infor.device = device
            infor.value = 0
            infor.device_pro = device_property
            infor.status = '1'
            infor.save()
        return HttpResponse(json.dumps({'handle':'success'}), content_type="application/json")
    except Exception as ex:
        return HttpResponse(json.dumps({'handle':'error',"msg": str(ex)}), content_type="application/json")
@login_required(login_url='/login')
@require_http_methods(["POST", ])
def edit(request):
    try:
        property_id = request.POST['property_id']
        device_property = DeviceProperties.objects.get(id=property_id)
        device_property.code = request.POST['code']
        device_property.name = request.POST['name']
        device_property.min = request.POST['min']
        device_property.max = request.POST['max']
        device_property.min_alarm  = request.POST['min_alarm']
        device_property.max_alarm = request.POST['max_alarm']
        device_property.symbol = request.POST['symbol']
        device_property.type = request.POST['type']
        device_property.m_type = request.POST['m_type']
        device_property.save()
        return HttpResponse(json.dumps({'handle':'success'}), content_type="application/json")
    except Exception as ex:
        return HttpResponse(json.dumps({'handle':'error',"msg": str(ex)}), content_type="application/json")
@login_required(login_url='/login')
@require_http_methods(["POST", ])
def delete(request):
    try:
        property_id = request.POST['property_id']
        device_property = DeviceProperties.objects.get(id=property_id)
        device_property.delete()
        return HttpResponse(json.dumps({'handle':'success'}), content_type="application/json")
    except Exception as ex:
        return HttpResponse(json.dumps({'handle':'error',"msg": str(ex)}), content_type="application/json")