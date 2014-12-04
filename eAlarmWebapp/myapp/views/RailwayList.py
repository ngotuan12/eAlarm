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
    devices = Device.objects.filter(type='1')
    context={'devices':devices}
    return render_to_response("railway/list.html", context, RequestContext(request))
@login_required(login_url='/login')
def add_railway(request):
    print('add')
@login_required(login_url='/login')
def edit_railway(request,railway_id):
    print('edit')
@login_required(login_url='/login')
def delete_railway(request,railway_id):
    print('delete')