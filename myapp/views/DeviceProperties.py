'''
Created on Apr 3, 2014

@author: TuanNA
'''
# @login_required(login_url='/signin')
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

from myapp.models import DeviceProperties


@login_required(login_url='/login')
def index(request):
	lsDeviceProperty = DeviceProperties.objects.all()
	context={'lsDeviceProperty':lsDeviceProperty}
	return render_to_response("device-property.html", context)