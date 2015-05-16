from django.shortcuts import render

import json
from django.http import HttpResponse
from django.views.generic import TemplateView
from djangolib.models import Book, Author, Style

from django.db.models import Count

from api.client import ApiClient
from api.models import RemoteInstance

class HomelibView(TemplateView):

    template_name = "djangolib/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomelibView, self).get_context_data(**kwargs)
        context['books'] = Book.objects.order_by('-id')[:10].values(
            'slug', 'filepath',
            'picture', 'author__name', 'author__slug', 'style__name',
            'style__slug')
        context['active'] = "homelib"
        styles = Style.objects.values('name').annotate(Count('book')).order_by(
            '-book__count')
        context['stats_styles'] = styles[:10]
        context['nb_author'] = Author.objects.all().count()
        context['nb_books'] = Book.objects.all().count()
        context['nb_styles'] = Style.objects.all().count()
        context['nb_peers'] = RemoteInstance.objects.all().count()
        return context
