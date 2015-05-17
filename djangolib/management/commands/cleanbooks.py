# -*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand
from djangolib.models import Book
from django.conf import settings
import os


class Command(NoArgsCommand):
    help = "Remove deleted books from database."

    def handle_noargs(self, **options):
        books = Book.objects.all()
        for book in books:
            relative_path = book.filepath
            if (relative_path[0] == "/"):
                relative_path = relative_path[1:]
            book_path = os.path.join(settings.MEDIA_ROOT, relative_path)
            if not os.path.isfile(book_path):
                self.stdout.write("- %s" % book_path)
                book.delete()
