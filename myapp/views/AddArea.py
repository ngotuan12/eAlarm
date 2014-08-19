'''
Created on Apr 3, 2014

@author: TuanNA
'''
# @login_required(login_url='/signin')
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response

from myapp.models import Area


@login_required(login_url='/login')
def index(request):
	if request.method == 'GET':
		try:
			lsArea = Area.objects.all()
			context={'lsArea':lsArea}
			context.update(csrf(request))
		except Exception as ex:
			context={}
			print(ex)
		finally:
			return render_to_response("add-area.html", context)
	elif request.method == 'POST':
		formType= request.POST['type']
		if formType == "addArea":
			context={}
			try:
				_code = request.POST['txtCode'].upper()
				_name = request.POST['txtName']
				_lat = float(request.POST['txtLat'])
				_lng = float(request.POST['txtLng'])
				_status = request.POST['slStatus']
				area = Area.objects.filter(code = _code)
				if len(area) >0 :
					raise Exception('Da ton tai !!!')
				lsArea = Area.objects.all()
				context={'lsArea':lsArea}
				context.update(csrf(request))
				return HttpResponseRedirect('/area')
			except Exception as ex:
				context.update({'has_error':ex,'code':_code,'name':'_name','status':_status})
				context.update(csrf(request))
				return render_to_response("add-area.html", context)
