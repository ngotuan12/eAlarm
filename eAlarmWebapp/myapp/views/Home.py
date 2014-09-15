'''
Created on Apr 3, 2014

@author: TuanNA
'''
# @login_required(login_url='/signin')
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from myapp.models import Device
from django.http.response import HttpResponseRedirect


@login_required(login_url='/login')
def index(request):
	return HttpResponseRedirect("/home")
@login_required(login_url='/login')
def home(request):
	if request.method == 'GET':
		try:
			_device_id = request.GET['device_id']
			devices = Device.objects.all()
			context={'devices':devices,'device_id':_device_id}
			return render_to_response("index.html", context, RequestContext(request))
		except Exception as ex:
			print(ex)
			devices = Device.objects.all()
			context={'devices':devices}
			return render_to_response("index.html", context, RequestContext(request))