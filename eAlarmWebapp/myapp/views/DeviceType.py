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


@login_required(login_url='/login')
def index(request):
    types = DeviceType.objects.all()
    context={'types':types}
    return render_to_response("device/device-type.html", context, RequestContext(request))
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