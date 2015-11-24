'''
Created on Dec 3, 2014

@author: TuanNA
'''
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from myapp.models.Area import Area
from myapp.models.Device import Device
from myapp.models.UserDevice import UserDevice


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