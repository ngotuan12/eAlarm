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
from myapp.models.DeviceTypeProperty import DeviceTypeProperty


@login_required(login_url='/login')
def index(request):
    types = DeviceType.objects.all()
    context={'types':types}
    return render_to_response("device/device-type.html", context, RequestContext(request))
@login_required(login_url='/login')
def device_type_properties(request):
    types = DeviceType.objects.all()
    properties = DeviceProperties.objects.raw("""
    select a.id,a.name, a.code , 
        (case when b.id is null then '0' else b.id end) device_type_property_id   
    from device_properties a
    left outer join device_type_property b on a.id = b.device_property_id
    and b.device_type_id = '1'
    where a.p_type = '2'
    """)
    context={'types':types,'properties':properties}
    return render_to_response("device/device-type-properties.html", context, RequestContext(request))
@login_required(login_url='/login')
@require_http_methods(["POST", ])
def get_device_type_properties(request):
    try:
        device_type_id = request.POST['device_type_id']
        lsProperties = DeviceProperties.objects.raw("""
            select a.id,a.name, a.code , 
                (case when b.id is null then '0' else b.id end) device_type_property_id   
            from device_properties a
            left outer join device_type_property b on a.id = b.device_property_id
            and b.device_type_id = %s
            where a.p_type = '2'
            """,[device_type_id])
        properties = []
        for pty in lsProperties:
            properties.append({
                               'id':pty.id,'code':pty.code,'name':pty.name,
                               'symbol':pty.symbol,'device_type_property_id':pty.device_type_property_id})
        return HttpResponse(json.dumps({'handle':'success','properties':properties}) , content_type="application/json")
    except Exception as ex:
        return HttpResponse(json.dumps({'handle':'error',"msg": str(ex)}), content_type="application/json")
@login_required(login_url='/login')
@require_http_methods(["POST", ])
def save_device_type_properties(request):
    try:
        device_type_id = request.POST['device_type_id']
        properties = request.POST.getlist('properties[]')
        DeviceTypeProperty.objects.filter(device_type_id = device_type_id).delete()
        for prt in properties:
            row = DeviceTypeProperty(device_type_id = device_type_id,property_id=prt)
            row.save()
        return HttpResponse(json.dumps({'handle':'success'}) , content_type="application/json")
    except Exception as ex:
        return HttpResponse(json.dumps({'handle':'error',"msg": str(ex)}), content_type="application/json")
@login_required(login_url='/login')
@require_http_methods(["POST", ])
def add_device_type(request):
    try:
        code = request.POST['code']
        name = request.POST['name']
        device_type = DeviceType()
        device_type.code = code
        device_type.name = name
        device_type.save()
        return HttpResponse(json.dumps({'handle':'success','id':device_type.id}) , content_type="application/json")
    except Exception as ex:
        return HttpResponse(json.dumps({'handle':'error',"msg": str(ex)}), content_type="application/json")
@login_required(login_url='/login')
@require_http_methods(["POST", ])
def edit_device_type(request):
    try:
        type_id = request.POST['id']
        code = request.POST['code']
        name = request.POST['name']
        device_type = DeviceType.objects.get(id=type_id)
        device_type.code = code
        device_type.name = name
        device_type.save()
        return HttpResponse(json.dumps({'handle':'success'}) , content_type="application/json")
    except Exception as ex:
        return HttpResponse(json.dumps({'handle':'error',"msg": str(ex)}), content_type="application/json")