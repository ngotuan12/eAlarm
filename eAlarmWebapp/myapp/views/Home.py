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
	context= {}
	if request.method == 'GET':
		try:
			devices = {}
			device_id = request.GET.get('device_id')
			status = request.GET.get('status')
			if device_id:
				devices = Device.objects.filter(id=device_id,type='1')
				context.update({'device_id':device_id})
			elif status:
				devices = Device.objects.filter(status=status,type='1')
			else: 
				devices = Device.objects.filter(type='1')
			context.update({'devices':devices})
			return render_to_response("index.html", context, RequestContext(request))
		except Exception as ex:
			print(ex)
			devices = Device.objects.all()
			context={'devices':devices}
			return render_to_response("index.html", context, RequestContext(request))