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

class BookView(TemplateView):

    template_name = "djangolib/books.html"

    def get_context_data(self, **kwargs):
        context = super(BookView, self).get_context_data(**kwargs)

        remote_instances = RemoteInstance.objects.all()
        books = []

        a_type = self.kwargs.get('type', None)

        if a_type == 'album':
            album = Album.objects.filter(slug=self.kwargs['key'])
            context['album'] = album
            books = Song.objects.filter(album__in=album).values(
                'title', 'slug', 'filepath', 'album__slug', 'album__name',
                'album__picture', 'artist__name', 'artist__slug',
                'style__name', 'style__slug')
            api_client = ApiClient()
            remote_songs = api_client.books(album=self.kwargs['key'],
                                            instances=remote_instances)
            try:
                books = self.merge_dict(books, remote_songs['books'])
            except KeyError:
                pass

        elif a_type == 'artist':
            artist = Artist.objects.filter(slug=self.kwargs['key'])
            context['artist'] = artist
            books = Song.objects.filter(artist=artist).order_by(
                'album__name').values(
                    'title', 'slug', 'filepath', 'album__slug', 'album__name',
                    'album__picture', 'artist__name', 'artist__slug',
                    'style__name', 'style__slug')

            api_client = ApiClient()
            remote_songs = api_client.books(artist=self.kwargs['key'],
                                            instances=remote_instances)
            try:
                books = self.merge_dict(books, remote_songs['books'])
            except KeyError:
                pass

        context['type'] = a_type
        context['books'] = books
        context['active'] = "books"
        return context

class AuthorView(TemplateView):
    pass

class StylesView(TemplateView):
    pass
