'''
Created on Dec 3, 2014

@author: TuanNA
'''
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from myapp.models import Device


@login_required(login_url='/login')
def index(request):
    devices = Device.objects.filter(type='4')
    context={'devices':devices}
    return render_to_response("railway/property.html", context, RequestContext(request))