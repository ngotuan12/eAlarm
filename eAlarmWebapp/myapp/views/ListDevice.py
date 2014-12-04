'''
Created on Apr 3, 2014

@author: TuanNA
'''
# @login_required(login_url='/signin')
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from myapp.models import Device


@login_required(login_url='/login')
@permission_required('myapp.view_device',login_url='/permission-error')
def index(request):
	devices = Device.objects.filter(type='1')
	context={'devices':devices}
	return render_to_response("list-device.html", context, RequestContext(request))