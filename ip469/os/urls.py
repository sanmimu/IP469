from django.conf.urls.defaults import *

urlpatterns = patterns(
    'ip469.os.views',
    # (r'^execute/(?P<cmd>.*)$', 'execute'),
    # (r'^$', 'default'),
    (r'^killself$', 'kill_ip469'),
)
