"""czaswolny URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from accounts.forms import *
from userena import views as userena_views
from reputation import views as reputation_views
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/signup/$', userena_views.signup, {'signup_form': SignupFormExtra}, name='userena_signup'),
    url(r'^accounts/signin/$', userena_views.signin, {'auth_form': AuthenticationFormExtra}, name='userena_signin'),
    url(r'^accounts/(?P<username>[\@\.\w-]+)/edit/$', userena_views.profile_edit, {'edit_profile_form': EditProfileFormExtra}, name='userena_profile_edit'),
    url(r'^accounts/(?P<username>[\@\.\w-]+)/reputation/$', reputation_views.show_received, name='reputation_show_received'),
    url(r'^accounts/(?P<username>[\@\.\w-]+)/reputation/given/$', reputation_views.show_given, name='reputation_show_given'),
    url(r'^accounts/(?P<username>[\@\.\w-]+)/reputation/add/$', reputation_views.add, name='reputation_add'),
    url(r'^accounts/', include('userena.urls')),
    url(r'^events/', include('events.urls'), name='events'),
    url(r'^accounts/addfriend/(?P<pk>[0-9]+)/$', views.addfriend, name='addfriend'),
    url(r'^accounts/invite/(?P<pk>[0-9]+)/$', views.invite, name='invite'),
    url(r'^accounts/refuseinvite/(?P<pk>[0-9]+)/$', views.refuseinvite, name='refuseinvite'),
    url(r'^accounts/unfriend/(?P<pk>[0-9]+)/$', views.unfriend, name='unfriend'),
    url(r'^accounts/uninvite/(?P<pk>[0-9]+)/$', views.uninvite, name='uninvite'),
    url(r'^posts/', include('posts.urls'), name='posts'),
    url(r'^$', views.home, name='home'),
    url(r'^about$', views.about, name='about'),
    url(r'^messages/', include('userena.contrib.umessages.urls')),
    url(r'^notifications/', include('notify.urls', 'notifications')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
