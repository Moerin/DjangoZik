from django.template.defaultfilters import slugify
from django.db import models


class Style(models.Model):

    """Docstring for Style. """

    name = models.CharField(max_length=250)
    slug = models.SlugField(db_index=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Style, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Author(models.Model):

    """Docstring for Author. """

    name = models.CharField(max_length=250)
    picture = models.CharField(max_length=256, null=True)
    text = models.TextField(null=True)
    slug = models.SlugField(db_index=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Author, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Book(models.Model):

    """Docstring for Book. """

    name = models.CharField(max_length=250)
    picture = models.CharField(max_length=256, null=True)
    author = models.ForeignKey(Author, related_name="book")
    style = models.ForeignKey(Style, related_name="book")
    filepath = models.CharField(max_length=256)
    text = models.TextField(null=True)
    slug = models.SlugField(db_index=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Book, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


