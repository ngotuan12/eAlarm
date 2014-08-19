from django.conf.urls import patterns, include, url
from django.contrib import admin

from eAlarm import settings
from myapp.views import Home,DeviceProperties,DeviceInfor


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^home$', Home.index),
    url(r'^device-property$', DeviceProperties.index),
    url(r'^device-infor$', DeviceInfor.index),
    url(r'^$', Home.index),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'signin.html'}, name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout',
                          {'next_page': 'login'}),
    url(regex=r'^(?P<path>.*)$', view='django.views.static.serve', kwargs={'document_root': settings.STATIC_ROOT, 'show_indexes' : False, }),
)
