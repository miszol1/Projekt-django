# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-06 19:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_event_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='author',
            field=models.IntegerField(default=3),
            preserve_default=False,
        ),
    ]