from django.conf.urls import patterns, url
from django.conf import settings

urlpatterns = patterns('blog.views',
    url(r'^$', 'home_page', name='home_page'),
    url(r'^new$', 'new_article', name='new_article'),
    url(r'^edit/([-\w]+)/$', 'edit_article', name='edit_article'),
    url(r'^delete/([-\w]+)/$', 'delete_article', name='delete_article'),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^500/$', 'django.views.generic.simple.direct_to_template', {'template': '500.html'}),
        url(r'^404/$', 'django.views.generic.simple.direct_to_template', {'template': '404.html'}),
    )