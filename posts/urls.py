from django.conf.urls import url

from . import views

app_name = 'posts'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create/(?P<pk>[0-9]+)/$', views.create, name='create'),
    url(r'^show/(?P<pk2>[0-9]+)/(?P<pk>[0-9]+)/$', views.details, name='details'),
    url(r'^destroy/(?P<pk2>[0-9]+)/(?P<pk>[0-9]+)/$', views.destroy, name='destroy'),
    url(r'^destroycomment/(?P<pk2>[0-9]+)/(?P<pk>[0-9]+)/(?P<pk3>[0-9]+)/$', views.destroycomment, name='destroycomment'),
    url(r'^createcomment/(?P<pk2>[0-9]+)/(?P<pk>[0-9]+)/$', views.createcomment, name='createcomment'),
    url(r'^like/(?P<pk2>[0-9]+)/(?P<pk>[0-9]+)/$', views.like, name='like'),
    url(r'^unlike/(?P<pk2>[0-9]+)/(?P<pk>[0-9]+)/$', views.unlike, name='unlike'),

]
