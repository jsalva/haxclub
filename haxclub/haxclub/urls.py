from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('haxclub.views',
    url(r'^$', 'index' ,name='hax-index'),
	url(r'^flatui/', include('flatui.urls',namespace='flatui')),
)
