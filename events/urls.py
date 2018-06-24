from django.conf.urls import url

from . import views

app_name = 'events'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^observing/$', views.observing, name='observing'),
    url(r'^show/(?P<pk>[0-9]+)/$', views.details, name='details'),
    url(r'^destroy/(?P<pk>[0-9]+)/$', views.destroy, name='destroy'),
    url(r'^join/(?P<pk>[0-9]+)/$', views.join, name='join'),
    url(r'^leave/(?P<pk>[0-9]+)/$', views.leave, name='leave'),
    url(r'^observe/(?P<pk>[0-9]+)/$', views.observe, name='observe'),
    url(r'^stopobserving/(?P<pk>[0-9]+)/$', views.stop_observing, name='stop_observing'),
    url(r'^block/(?P<pk>[0-9]+)/(?P<user_id>[0-9]+)/$', views.block, name='block'),
    url(r'^unblock/(?P<pk>[0-9]+)/(?P<user_id>[0-9]+)/$', views.unblock, name='unblock'),
    url(r'^create/$', views.create, name='create'),
    url(r'^like/(?P<pk>[0-9]+)/$', views.like, name='like'),
    url(r'^unlike/(?P<pk>[0-9]+)/$', views.unlike, name='unlike'),

]
