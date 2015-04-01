'''
Created on Dec 3, 2014

@author: TuanNA
'''
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from myapp.models.Device import Device


@login_required(login_url='/login')
def monitor(request):
    context = {}
    #devices = Device.objects.filter(type='4')
    #context.update({'devices':devices})
    try: 
        devices = Device.objects.filter(type='4')
        context.update({'devices':devices})
        return render_to_response("railway/monitor.html", context, RequestContext(request))
    except Exception as ex:
        print(ex)
        devices = Device.objects.all()
        context = {'devices':devices}
        return render_to_response("railway/monitor.html", context, RequestContext(request))
