'''
Created on Aug 26, 2014

@author: TuanNA
'''
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User, Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.core.context_processors import csrf


@login_required(login_url='/login')
def change_password(request):
    return ""
@user_passes_test(lambda u: u.is_superuser,login_url='/permission-error',redirect_field_name=None)
def reset_password(request):
    return ""
@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser,login_url='/permission-error',redirect_field_name=None)
def view_user(request):
    users = User.objects.all().order_by("username")
    context ={"users":users}
    return render_to_response("user/user.html",context, RequestContext(request))
@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser,login_url='/permission-error',redirect_field_name=None)
def add_user(request):
    context ={}
    return render_to_response("user/add-user.html",context, RequestContext(request))
@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser,login_url='/permission-error',redirect_field_name=None)
def change_user(request,user_id):
    try:
        content_types = ContentType.objects.filter(app_label = "myapp")
        permissions = Permission.objects.filter(content_type__in=content_types).order_by('content_type__id','-codename')
        groups = Group.objects.all()
        current_user = User.objects.get(id=user_id)
        current_pers = current_user.user_permissions.values_list('id', flat=True)
        current_groups = current_user.groups.values_list('id', flat=True)
        context ={'current_user': current_user,'current_groups':current_groups,'current_pers':current_pers,'permissions':permissions,'groups':groups}
        if request.POST:
            return HttpResponseRedirect('/user')
        context.update(csrf(request))
        return render_to_response("user/change-user.html",context, RequestContext(request))
    except User.DoesNotExist:
        return HttpResponseRedirect("/notfound-error")
@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser,login_url='/permission-error',redirect_field_name=None)
def delete_user(request,user_id):
    return HttpResponseRedirect("/user")