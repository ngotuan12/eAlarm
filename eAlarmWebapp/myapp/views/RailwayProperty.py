'''
Created on Dec 3, 2014

@author: TuanNA
'''
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext

@login_required(login_url='/login')
def index(request):
    context= {}
    return render_to_response("railway/property.html", context, RequestContext(request))