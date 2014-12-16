'''
Created on Dec 3, 2014

@author: TuanNA
'''
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from myapp.models import Device


@login_required(login_url='/login')
def index(request):
    devices = Device.objects.filter(type='4')
    context={'devices':devices}
    context.update(csrf(request))
    return render_to_response("log/view-log.html", context, RequestContext(request))