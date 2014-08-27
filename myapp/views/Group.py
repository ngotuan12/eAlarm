'''
Created on Aug 26, 2014

@author: TuanNA
'''
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User, Group
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext


@user_passes_test(lambda u: u.is_superuser,login_url='/permission-error',redirect_field_name=None)
def view_group(request):
    groups = Group.objects.all().order_by("name")
    context ={"groups":groups}
    return render_to_response("group/group.html",context, RequestContext(request))
@user_passes_test(lambda u: u.is_superuser,login_url='/permission-error',redirect_field_name=None)
def add_group(request):
    context ={}
    return render_to_response("group/add-group.html",context, RequestContext(request))
@user_passes_test(lambda u: u.is_superuser,login_url='/permission-error',redirect_field_name=None)
def change_group(request,user_id):
    try:
        current_user = User.objects.get(id=user_id)
        context ={'current_user': current_user}
        return render_to_response("group/change-group.html",context, RequestContext(request))
    except User.DoesNotExist:
        return HttpResponseRedirect("/notfound-error")
@user_passes_test(lambda u: u.is_superuser,login_url='/permission-error',redirect_field_name=None)
def delete_group(request):
    return HttpResponseRedirect("/group")