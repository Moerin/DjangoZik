from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.contrib import admin

from djangolib.views import HomelibView

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^lib$',
                           login_required(HomelibView.as_view()),
                           name='homelib'),
                       )
