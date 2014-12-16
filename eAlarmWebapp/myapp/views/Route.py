'''
Created on Apr 3, 2014

@author: TuanNA
'''
# @login_required(login_url='/signin')
from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from myapp.models import Route


@login_required(login_url='/login')
@permission_required('myapp.view_device',login_url='/permission-error')
def index(request):
	try:
		routes = Route.objects.all()
		context={'routes':routes}
		context.update(csrf(request))
	except Exception as ex:
		context={}
		print(ex)
	finally:
		return render_to_response("railway/route.html", context,RequestContext(request))
@login_required(login_url='/login')
@permission_required('myapp.view_device',login_url='/permission-error')
def add_route(request):
	context={}
	context.update(csrf(request))
	try:
		if request.method == 'POST':
			_code =request.POST['txtCode'].strip()
			_name =request.POST['txtName'].strip()
			route =Route()
			route.code=_code
			route.name=_name
			route.save()
			return HttpResponseRedirect('/railway/route/')
	except Exception as ex:
		print(ex)
	finally:
		return render_to_response("railway/add-route.html", context,RequestContext(request))
def edit_route(request,route_id):
	try:
		route = Route.objects.get(id=route_id)
		context={'route':route}
		context.update(csrf(request))
		if request.method == 'POST':
			_code =request.POST['txtCode'].strip()
			_name =request.POST['txtName'].strip()
			route.code=_code
			route.name=_name
			route.save()
			return HttpResponseRedirect('/railway/route/')
	except Exception as ex:
		context={}
		print(ex)
	finally:
		return render_to_response("railway/edit-route.html", context,RequestContext(request))
def delete_route(request,route_id):
	try:
		routes = Route.objects.all()
		context={'routes':routes}
		context.update(csrf(request))
	except Exception as ex:
		context={}
		print(ex)
	finally:
		return render_to_response("railway/add-route.html", context,RequestContext(request))