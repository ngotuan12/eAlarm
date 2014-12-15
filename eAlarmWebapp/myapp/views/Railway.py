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
    if request.method == 'GET':
        try:
            devices = {}
            device_id = request.GET.get('device_id')
            status = request.GET.get('status')
            if device_id:
                devices = Device.objects.filter(id=device_id, type='4')
                context.update({'device_id':device_id})
            elif status:
                devices = Device.objects.filter(status=status, type='4')
            else: 
                devices = Device.objects.filter(type='4')
            context.update({'devices':devices})
            return render_to_response("railway/monitor.html", context, RequestContext(request))
        except Exception as ex:
            print(ex)
            devices = Device.objects.all()
            context = {'devices':devices}
            return render_to_response("railway/monitor.html", context, RequestContext(request))
