# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-13 20:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
        ('events', '0005_auto_20171106_2014'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='posts',
            field=models.ManyToManyField(to='posts.Post'),
        ),
    ]