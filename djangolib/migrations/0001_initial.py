# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('picture', models.CharField(max_length=256, null=True)),
                ('text', models.TextField(null=True)),
                ('slug', models.SlugField()),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('picture', models.CharField(max_length=256, null=True)),
                ('filepath', models.CharField(max_length=256)),
                ('text', models.TextField(null=True)),
                ('slug', models.SlugField()),
                ('author', models.ForeignKey(related_name='book', to='djangolib.Author')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Style',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('slug', models.SlugField()),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='book',
            name='style',
            field=models.ForeignKey(related_name='book', to='djangolib.Style'),
        ),
    ]
