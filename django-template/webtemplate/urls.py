from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

from webtemplate.apps.homepage.views import *

admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    url(r'^$', HomepageView.as_view(), name='homepage-index')
)

if getattr(settings, 'MANAGING_STATIC_FILES', False):
    urlpatterns += patterns(
        '',
        (
            r'^static/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT}
        )
    )

