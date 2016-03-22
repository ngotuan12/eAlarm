'''
Created on Dec 3, 2014

@author: TuanNA
'''
from datetime import datetime
import json

from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.forms.models import model_to_dict
from django.http.response import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.decorators.http import require_http_methods

from myapp.models.Area import Area
from myapp.models.Device import Device
from myapp.models.RailwaySession import RailwaySession
from myapp.models.RailwaySessionDetail import RailwaySessionDetail
from myapp.models.UserDevice import UserDevice
from myapp.util import DateEncoder


@login_required(login_url='/login')
def monitor(request):
    context = {}
    #devices = Device.objects.filter(type='4')
    #context.update({'devices':devices})
    try:
        devices = []
        if request.user.is_superuser:
            devices = Device.objects.filter(type='4').order_by('route__order','order')
        else:
            #test_ids = list(TestSubjectSet.objects.all().values_list('test_id', flat=True))
            user_device = list(UserDevice.objects.filter(user=request.user).values_list('device_id', flat=True))
            devices = Device.objects.filter(id__in=user_device).order_by('route__order','order')
        context.update({'devices':devices})
        return render_to_response("railway/monitor.html", context, RequestContext(request))
    except Exception as ex:
        print(ex)
        devices = Device.objects.all()
        context = {'devices':devices}
        return render_to_response("railway/monitor.html", context, RequestContext(request))
@login_required(login_url='/login')
def monitorV2(request):
    context = {}
    #devices = Device.objects.filter(type='4')
    #context.update({'devices':devices})
    try:
        devices = []
        if request.user.is_superuser:
            devices = Device.objects.filter(type='4').order_by('route__order','order')
        else:
            #test_ids = list(TestSubjectSet.objects.all().values_list('test_id', flat=True))
            user_device = list(UserDevice.objects.filter(user=request.user).values_list('device_id', flat=True))
            devices = Device.objects.filter(id__in=user_device).order_by('route__order','order')
        context.update({'devices':devices})
        return render_to_response("railway/monitorV2.html", context, RequestContext(request))
    except Exception as ex:
        print(ex)
        devices = Device.objects.all()
        context = {'devices':devices}
        return render_to_response("railway/monitorV2.html", context, RequestContext(request))
@login_required(login_url='/login')
def maps(request):
    try:
        lsArea = Area.objects.filter(level = '2')
        lsDevice  = Device.objects.filter(type='4')
        context={'lsArea':lsArea,'lsDevice':lsDevice}
        context.update(csrf(request))
    except Exception as ex:
        context={}
        print(ex)
    finally:
        return render_to_response("railway-map.html", context,RequestContext(request))
def vinh(request):
    try:
        context = {}
        devices = Device.objects.filter(type='4')
        context.update({'devices':devices})
        return render_to_response("railway/vinh.html", context, RequestContext(request))
    except Exception as ex:
        print(ex)
        devices = Device.objects.all()
        context = {'devices':devices}
        return render_to_response("railway/vinh.html", context, RequestContext(request))
@login_required(login_url='/login')
def railway_manager(request):
    context = {}
    try:
        devices = []
        devices = Device.objects.filter(type='4').order_by('route__order','order')
        context.update({'devices':devices})
        return render_to_response("railway/railway_manager.html", context, RequestContext(request))
    except Exception as ex:
        print(ex)
@login_required(login_url='/login')
@require_http_methods(["POST", ])
def getRailwayHistory(request):
    try:
        device_id = request.POST['device_id']
        device = Device.objects.get(id=device_id)
        histories = RailwaySession.objects.filter(device=device).order_by('-start_date')
        railway_sessions = []
        for history in histories:
            railway_sessions.append(model_to_dict(history))
        return HttpResponse(json.dumps({'handle':'success','railway_histories':railway_sessions}, cls=DateEncoder.DateTimeEncoder) , content_type="application/json")
    except Exception as ex:
        return HttpResponse(json.dumps({'handle':'error',"msg": str(ex)}), content_type="application/json")
@login_required(login_url='/login')
@require_http_methods(["POST", ])
def deleteRailwayHistory(request):
    try:
        history_id = request.POST['history_id']
        history = RailwaySession.objects.get(id=history_id)
        history.delete()
        return HttpResponse(json.dumps({'handle':'success'}) , content_type="application/json")
    except Exception as ex:
        return HttpResponse(json.dumps({'handle':'error',"msg": str(ex)}), content_type="application/json")
@login_required(login_url='/login')
@require_http_methods(["POST", ])
def editRailwayHistory(request):
    try:
        history_id = request.POST['history_id']
        strStartDate = request.POST['start_date']
        strEndDate = request.POST['end_date']
        history = RailwaySession.objects.get(id=history_id)
        history.start_date = datetime.strptime(strStartDate, '%d/%m/%Y %H:%M:%S')
        history.end_date = datetime.strptime(strEndDate, '%d/%m/%Y %H:%M:%S')
        history.save()
        return HttpResponse(json.dumps({'handle':'success'}) , content_type="application/json")
    except Exception as ex:
        return HttpResponse(json.dumps({'handle':'error',"msg": str(ex)}), content_type="application/json")
@login_required(login_url='/login')
@require_http_methods(["POST", ])
def editRailwayHistoryDetail(request):
    try:
        detail_id = request.POST['detail_id']
        strValue = request.POST['detail_value']
        history_detail = RailwaySessionDetail.objects.get(id=detail_id)
        history_detail.value = strValue
        history_detail.save()
        return HttpResponse(json.dumps({'handle':'success'}) , content_type="application/json")
    except Exception as ex:
        return HttpResponse(json.dumps({'handle':'error',"msg": str(ex)}), content_type="application/json")