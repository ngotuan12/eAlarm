from django.conf.urls import patterns, include, url
from django.contrib import admin

from eAlarmWebapp import settings
from myapp.views import Home, DeviceProperties, AddDeviceProperties, EditDeviceProperties, Area, AddArea, DeviceInfor, EditArea\
, Device, User, Error, Group, ListDevice, AddDevice, EditDevice, Report, Railway, \
    RailwayList, RailwayProperty


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^home$', Home.home),
    #railway
    url(r'^railway/monitor/$', Railway.monitor,name='railway-monitor'),
    url(r'^railway/list/$', RailwayList.index,name='railway-list'),
    url(r'^railway/property/$', RailwayProperty.index,name='railway-property'),
    #add,edit,delete railway
    url(r'^railway/list/add/$', RailwayList.add_railway,name='railway-list-add'),
    url(r'^railway/list/edit/(?P<railway_id>\w+)/$', RailwayList.edit_railway,name='railway-list-edit'),
    url(r'^railway/list/delete/(?P<railway_id>\w+)/$', RailwayList.delete_railway,name='railway-list-delete'),
     #add,edit,delete property
    url(r'^railway/property/add/$', RailwayProperty.add_property,name='railway-property-add'),
    url(r'^railway/property/edit/(?P<property_id>\w+)/$', RailwayProperty.edit_property,name='railway-property-edit'),
    url(r'^railway/property/delete/(?P<property_id>\w+)/$', RailwayProperty.delete_property,name='railway-property-delete'),
    #get_property
    url(r'^get-property/(?P<p_code>\w+)/$', RailwayProperty.get_property, name='get-property'),
    #machine room
    url(r'^device-infor$', DeviceInfor.index),
    url(r'^$', Home.index),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^password/change/$', 'django.contrib.auth.views.password_change', {'template_name': 'change-password.html'}, name='password_change'),
    url(r'^password/change/done/$',
                    'django.contrib.auth.views.password_change_done', {'template_name': 'change-password-done.html'},
                    name='password_change_done'),
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'signin.html'}, name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': 'login'}),
    url(r'^device-property$', DeviceProperties.index),
    url(r'^add-device-property$', AddDeviceProperties.index,name='add-device-property'),
    url(r'^edit-device-property$', EditDeviceProperties.index,name='add-device-property'),
	url(r'^area$', Area.index),
    url(r'^add-area$', AddArea.index),
    url(r'^add-area$', AddArea.index,name='add-area'),
    url(r'^edit-area$', EditArea.index),
    url(r'^device$', Device.index),
    url(r'^device-list$', ListDevice.index),
    url(r'^add-device', AddDevice.index),
    url(r'^add-device', AddDevice.index,name='add-device'),
    url(r'^edit-device', EditDevice.index),
    url(r'^edit-device', EditDevice.index,name='edit-device'),
    
    # User
    url(r'^user$', User.view_user,name='user'),
    url(r'^user/add/$', User.add_user,name='delete-user'),
    url(r'^user/delete/(?P<user_id>\w+)/$', User.delete_user,name='add-user'),
    url(r'^user/(?P<user_id>\w+)/$', User.change_user,name='change-user'),
    # Group
    url(r'^group$', Group.view_group,name='user'),
    url(r'^group/add/$', Group.add_group,name='add-group'),
    url(r'^group/delete/(?P<group_id>\w+)/$', Group.delete_group,name='delete-group'),
    url(r'^group/(?P<group_id>\w+)/$', Group.change_group,name='change-group'),
    # Device Report
    url(r'^device-report$', Report.view_device_report,name='device-report'),
    url(r'^device-detail-report$', Report.view_device_detail_report,name='device-detail-report'),
    url(r'^device-error-report$', Report.view_device_error_report,name='device-error-report'),
    url(r'^sensor-mirror-report/$', Report.view_sensor_mirror_report,name='sensor-mirror-report'),
    # Device Detail Report
    url(r'^group$', Group.view_group,name='user'),
    url(r'^permission-error$', Error.permission_error,name='permission-error'),
    url(r'^notfound-error$', Error.notfound_error,name='notfound-error'),
    url(regex=r'^report/(?P<path>.*)$', view='django.views.static.serve', kwargs={'document_root': settings.REPORT_ROOT, 'show_indexes' : True, }),
    url(regex=r'^(?P<path>.*)$', view='django.views.static.serve', kwargs={'document_root': settings.STATIC_ROOT, 'show_indexes' : True, }),
)
