from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.contrib import admin

from djangolib.views import HomelibView, BookView, AuthorView, StylesView

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^lib$',
                           login_required(HomelibView.as_view()),
                           name='homelib'),
                       url(r'^lib/books/',
                           login_required(BookView.as_view()),
                           name='books'),
                       url(r'^lib/books/(?P<type>[^/]+)/(?P<key>[^/]+)$',
                           login_required(BookView.as_view()),
                           name='books'),
                       url(r'^/lib/author/(?P<style>[^/]+)?$',
                           login_required(AuthorView.as_view()),
                           name='author'),
                       url(r'^/lib/styles/(?P<style>[^/]+)?$',
                           login_required(StylesView.as_view()),
                           name='libstyles')
                       )
