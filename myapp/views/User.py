'''
Created on Aug 26, 2014

@author: TuanNA
'''
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext


def change_password(request):
    return ""
@user_passes_test(lambda u: u.is_superuser,login_url='/permission-error',redirect_field_name=None)
def reset_password(request):
    return ""
@user_passes_test(lambda u: u.is_superuser,login_url='/permission-error',redirect_field_name=None)
def view_user(request):
    users = User.objects.all().order_by("username")
    context ={"users":users}
    return render_to_response("user/user.html",context, RequestContext(request))
@user_passes_test(lambda u: u.is_superuser,login_url='/permission-error',redirect_field_name=None)
def add_user(request):
    context ={}
    return render_to_response("user/add-user.html",context, RequestContext(request))
@user_passes_test(lambda u: u.is_superuser,login_url='/permission-error',redirect_field_name=None)
def change_user(request,user_id):
    try:
        current_user = User.objects.get(id=user_id)
        context ={'current_user': current_user}
        return render_to_response("user/change-user.html",context, RequestContext(request))
    except User.DoesNotExist:
        return HttpResponseRedirect("/notfound-error")
@user_passes_test(lambda u: u.is_superuser,login_url='/permission-error',redirect_field_name=None)
def delete_user(request,user_id):
    return HttpResponseRedirect("/user")