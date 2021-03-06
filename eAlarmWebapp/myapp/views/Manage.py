# -*- coding: utf8 -*-
'''
Created on Dec 3, 2014

@author: TuanNA
'''
import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.http.response import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.decorators.http import require_http_methods

from myapp.models.Device import Device
from myapp.models.UserDevice import UserDevice
from myapp.util import DateEncoder
from myapp.models.Route import Route


@login_required(login_url='/login')
def assign_railway(request):
    context = {}
    users = User.objects.all().order_by("username")
    context.update({"users":users})
    #devices = Device.objects.filter(type='4')
    #context.update({'devices':devices})
    try: 
        devices = Device.objects.filter(type='4').order_by('route__id')
        context.update({'devices':devices})
        return render_to_response("manage/assign_railway.html", context, RequestContext(request))
    except Exception as ex:
        print(ex)
        devices = Device.objects.all()
        context = {'devices':devices}
        return render_to_response("manage/assign_railway.html", context, RequestContext(request))
@login_required(login_url='/login')
def railway_order(request):
    context = {}
    routes = Route.objects.all().order_by('order')
    context.update({"routes":routes})
    return render_to_response("manage/railway_order.html", context, RequestContext(request))
@login_required(login_url='/login')
@require_http_methods(["POST", ])
def downOrderRoute(request):
    try:
        route_id = request.POST['route_id']
        routes = Route.objects.all().order_by('order')
        i = 0
        cur_route = None;
        next_route = None;
        for  i in range(len(routes)):
            routes[i].order = i
            if(str(routes[i].id) == route_id):
                cur_route = routes[i]
                next_route = routes[i+1]
            else:
                routes[i].save()
        if next_route is not None:
            temp = cur_route.order;
            cur_route.order = next_route.order
            next_route.order = temp
            cur_route.save()
            next_route.save()
        return HttpResponse(json.dumps({'handle':'success'}, cls=DateEncoder.DateTimeEncoder) , content_type="application/json")
    except Exception as ex:
        return HttpResponse(json.dumps({'handle':'error',"msg": str(ex)}), content_type="application/json")
@login_required(login_url='/login')
@require_http_methods(["POST", ])
def upOrderRoute(request):
    try:
        route_id = request.POST['route_id']
        routes = Route.objects.all().order_by('order')
        i = 0
        cur_route = None;
        prev_route = None;
        for  i in range(len(routes)):
            routes[i].order = i
            if(str(routes[i].id) == route_id):
                cur_route = routes[i]
                prev_route = routes[i-1]
            else:
                routes[i].save()
        if prev_route is not None:
            temp = cur_route.order;
            cur_route.order = prev_route.order
            prev_route.order = temp
            cur_route.save()
            prev_route.save()
        return HttpResponse(json.dumps({'handle':'success'}, cls=DateEncoder.DateTimeEncoder) , content_type="application/json")
    except Exception as ex:
        return HttpResponse(json.dumps({'handle':'error',"msg": str(ex)}), content_type="application/json")
@login_required(login_url='/login')
@require_http_methods(["POST", ])
def downOrderDevice(request):
    try:
        route_id = request.POST['route_id']
        device_id = request.POST['device_id']
        devices = Device.objects.filter(route_id = route_id).order_by('order')
        cur_device = None;
        next_device = None;
        for i in range(len(devices)):
            devices[i].order = i
            if(str(devices[i].id) == device_id):
                cur_device = devices[i]
                next_device = devices[i+1]
            else:
                devices[i].save()
        if next_device is not None:
            temp = cur_device.order;
            cur_device.order = next_device.order
            next_device.order = temp
            cur_device.save()
            next_device.save()
        return HttpResponse(json.dumps({'handle':'success'}, cls=DateEncoder.DateTimeEncoder) , content_type="application/json")
    except Exception as ex:
        return HttpResponse(json.dumps({'handle':'error',"msg": str(ex)}), content_type="application/json")
@login_required(login_url='/login')
@require_http_methods(["POST", ])
def upOrderDevice(request):
    try:
        route_id = request.POST['route_id']
        device_id = request.POST['device_id']
        devices = Device.objects.filter(route_id = route_id).order_by('order')
        cur_device = None;
        prev_device = None;
        for i in range(len(devices)):
            devices[i].order = i
            if(str(devices[i].id) == device_id):
                cur_device = devices[i]
                prev_device = devices[i-1]
            else:
                devices[i].save()
        if prev_device is not None:
            temp = cur_device.order;
            cur_device.order = prev_device.order
            prev_device.order = temp
            cur_device.save()
            prev_device.save()
        return HttpResponse(json.dumps({'handle':'success'}, cls=DateEncoder.DateTimeEncoder) , content_type="application/json")
    except Exception as ex:
        return HttpResponse(json.dumps({'handle':'error',"msg": str(ex)}), content_type="application/json")
@login_required(login_url='/login')
def railway_statistics(request):
    context = {}
    devices = []
    if request.user.is_superuser:
        devices = Device.objects.filter(type='4').order_by('route__order','order')
    else:
        #test_ids = list(TestSubjectSet.objects.all().values_list('test_id', flat=True))
        user_device = list(UserDevice.objects.filter(user=request.user).values_list('device_id', flat=True))
        devices = Device.objects.filter(id__in=user_device).order_by('route__order','order')
    context.update({'devices':devices})
    return render_to_response("manage/railway_statistics.html", context, RequestContext(request))
@login_required(login_url='/login')
@require_http_methods(["POST", ])
def getDeviceByRoute(request):
    try:
        route_id = request.POST['route_id']
        all_device = Device.objects.filter(route_id=route_id).order_by('order')
        devices = []
        for device in all_device:
            devices.append(model_to_dict(device))
        return HttpResponse(json.dumps({'handle':'success','devices':devices}, cls=DateEncoder.DateTimeEncoder) , content_type="application/json")
    except Exception as ex:
        return HttpResponse(json.dumps({'handle':'error',"msg": str(ex)}), content_type="application/json")
@login_required(login_url='/login')
@require_http_methods(["POST", ])
def getAssignDeviceByUser(request):
    try:
        user_id = request.POST['user_id']
        user = User.objects.get(id=user_id)
        user_device = UserDevice.objects.filter(user=user).order_by('device__route__id')
        devices = []
        for userDevice in user_device:
            devices.append({'code':userDevice.device.code,'id':userDevice.device.id,'name':userDevice.device.name,'route':model_to_dict(userDevice.device.route)})
        return HttpResponse(json.dumps({'handle':'success','devices':devices}, cls=DateEncoder.DateTimeEncoder) , content_type="application/json")
    except Exception as ex:
        return HttpResponse(json.dumps({'handle':'error',"msg": str(ex)}), content_type="application/json")
@login_required(login_url='/login')
@require_http_methods(["POST", ])
def assignDeviceToUser(request):
    try:
        user_id = request.POST['user_id']
        device_id = request.POST['device_id']
        try:
            UserDevice.objects.get(user_id=user_id,device_id=device_id)
            return HttpResponse(json.dumps({'handle':'error',"msg": "Đường ngang đã có trong danh sách"}), content_type="application/json")
        except UserDevice.DoesNotExist:
            UserDevice.objects.create(user_id=user_id,device_id=device_id)
            return HttpResponse(json.dumps({'handle':'success'}), content_type="application/json")
    except Exception as ex:
        return HttpResponse(json.dumps({'handle':'error',"msg": str(ex)}), content_type="application/json")
@login_required(login_url='/login')
@require_http_methods(["POST", ])
def unsignDeviceFromUser(request):
    try:
        user_id = request.POST['user_id']
        device_id = request.POST['device_id']
        userDevice = UserDevice.objects.get(user_id=user_id,device_id=device_id)
        if userDevice is None:
            return HttpResponse(json.dumps({'handle':'error',"msg": "Đường ngang không hợp lệ"}), content_type="application/json")
        userDevice.delete()
        return HttpResponse(json.dumps({'handle':'success'}), content_type="application/json")
    except Exception as ex:
        return HttpResponse(json.dumps({'handle':'error',"msg": str(ex)}), content_type="application/json")
def balance(request):
    context = {}
    devices = Device.objects.filter(type='4').order_by('route__order','order')
    context.update({'devices':devices})
    return render_to_response("manage/balance.html", context, RequestContext(request))