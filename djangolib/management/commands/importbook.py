# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.utils.encoding import smart_text
from django.conf import settings
from djangolib.models import Book, Author, Style
from infos_grabber.metadataGrabber import MetadataGrabber
from optparse import make_option
import re
import os
import pdfminer
#import mutagen


class Command(BaseCommand):
    help = "Scan book folder and add new books."
    option_list = BaseCommand.option_list + (make_option('--verbose',
                                                         action='store_true',
                                                         dest='verbose',
                                                         default=False,
                                                         help='Verbose mode'), )

    def handle(self, *args, **options):

        self.stdout.write("Cleaning old books")
        if options['verbose']:
            self.stdout.write("Scanning : %s" % settings.MEDIA_ROOT)
        else:
            self.stdout.write("Scanning music folder")
        books = []
        for root, dirs, files in os.walk(settings.MEDIA_ROOT):
            for filename in files:
                if not filename.endswith(
                    ('.pdf', 'epub')) or filename.startswith('.'):
                    continue

                books.append(os.path.join(root, filename))

                book = os.path.join(root, filename)

                # If book exists, skip to the next
                book_path = book.replace(settings.MEDIA_ROOT, '')
                nb_book = Book.objects.filter(filepath=book_path).count()
                if (nb_book > 0):
                    if options['verbose']:
                        self.stdout.write("skip %s " %
                                          book_path.decode('utf-8', 'ignore'))
                    continue

                tags = self.get_tags(book)

                # Check if a similar book exists
                try:
                    author = Author.objects.filter(name=tags['author'])
                    new_book = Book.objects.filter(title=tags['name'],
                                                   author=author)
                    if new_book.count() > 0:
                        continue
                except:
                    pass

                # Visual output
                if options['verbose']:
                    frmt_str = "+ %s : %s (%s, %s)"
                    self.stdout.write(
                        frmt_str % (tags['author'].decode('utf-8', 'replace'),
                                    tags['title'].decode('utf-8', 'replace'),
                                    tags['genre'].decode('utf-8', 'replace')))

                # Create author if not exists
                author = self.create_author(tags['author'], None)

                # Create style if not exists
                style = self.create_style(tags['genre'])

                bookpath = smart_text(book.replace(settings.MEDIA_ROOT, ''))

                if (bookpath[0] == "/"):
                    bookpath = bookpath[1:]

                self.create_book(tags['title'], author, style, bookpath)

        self.stdout.write("Book scan finished")

        # Import authors
        self.stdout.write("Import authors")
        ImportAuthor.import_authors()

        # Import covers
        self.stdout.write("Import covers")
        ImportCovers.import_covers()

        self.stdout.write("Scan finished")

    def create_author(self, author, picture):
        author, created = Author.objects.get_or_create(name=author,
                                                       picture=picture)
        if created:
            author.save()
        return author

    def create_style(self, name):
        style, created = Style.objects.get_or_create(name=name)
        if created:
            style.save()
        return style

    def create_book(self, name, author, style, book):
        book, created = Book.objects.get_or_create(title=title,
                                                   author=author,
                                                   style=style,
                                                   filepath=book)
        if created:
            book.save()
        return book

    # TODO rename get_info
    def get_tags(self, book):
        title = book.decode('utf-8', 'ignore').split('/')[-1]
        date = "0001-01-01"
        genre = "Unknown"
        author = "Unknown"

        try:
            # TODO change mutagen for pdfminer http://stackoverflow.com/questions/14209214/reading-the-pdf-properties-metadata-in-python
            book = mutagen.File(smart_text(book), easy=True)
            if "name" in book.keys():
                name = book['name'][0].encode('utf-8').strip().capitalize()
            if "date" in book.keys():
                date = "%s-01-01" % book['date'][0].encode('utf-8').strip()
                regex = re.compile("^([0-9]{4}-[0-9]{2}-[0-9]{2})$")
                if not regex.match(date) or date == "0000-01-01":
                    date = None
            if "genre" in book.keys():
                genre = book['genre'][0].encode('utf-8').strip().capitalize()
            if "author" in book.keys():
                author = book['author'][0].encode('utf-8').strip().capitalize()
        except:
            # Use default values
            pass

        return {
            'name': name,
            'date': date,
            'genre': genre,
            'author': author
        }


class ImportAuthor():
    @staticmethod
    def import_authors():
        # Artists without pictures are considered as "new"
        authors = Author.objects.filter(picture=None)
        metadata_grabber = MetadataGrabber()
        for author in authors:
            try:
                infos = metadata_grabber.get_and_save_author(
                    author.name, "%s/%s" % (settings.STATIC_PATH,
                                            'images/authors/'),
                    "%s.jpg" % author.slug)
                if infos is not None:
                    if 'infos' in infos.keys() and 'text' in infos['infos'].keys(
                    ) and infos['infos']['text'] is not None:
                        author.text = infos['infos']['text']
                    else:
                        author.text = ""
                    if author.slug is not None:
                        author.picture = 'images/authors/%s.jpg' % author.slug
                    else:
                        author.picture = 'images/no_band.jpg'
                    author.save()
            except:
                author.picture = 'images/no_band.jpg'
                author.text = ""
                author.save()


class ImportCovers():
    @staticmethod
    def import_covers():
        # Albums with no cover are considered as "new"
        books = Book.objects.filter(picture=None)
        metadata_grabber = MetadataGrabber()
        for book in books:
            image = metadata_grabber.get_and_save_cover(
                "%s" % book.name, "%s/%s" % (settings.STATIC_PATH,
                                              'images/covers/'),
                "%s.jpg" % book.slug)
            if image is not None:
                path = "%s%s.jpg" % ("images/covers/", book.slug)
            else:
                path = "images/no_cover.gif"
            book.picture = path
            book.save()
