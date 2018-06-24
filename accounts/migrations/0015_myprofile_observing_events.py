# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-17 19:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_event_blacklist'),
        ('accounts', '0014_auto_20180117_1823'),
    ]

    operations = [
        migrations.AddField(
            model_name='myprofile',
            name='observing_events',
            field=models.ManyToManyField(blank=True, null=True, to='events.Event'),
        ),
    ]
