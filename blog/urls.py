from django.conf.urls import patterns, url
from django.conf import settings

from blog import views

urlpatterns = patterns('',
    url(r'^$', views.home_page, name='home_page'),
    url(r'^new$', views.new_article, name='new_article'),
    url(r'^edit/([-\w]+)/$', views.edit_article, name='edit_article'),
    url(r'^delete/([-\w]+)/$', views.delete_article, name='delete_article'),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^500/$', 'django.views.generic.simple.direct_to_template', {'template': '500.html'}),
        url(r'^404/$', 'django.views.generic.simple.direct_to_template', {'template': '404.html'}),
    )