# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-17 18:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_merge_20180109_2012'),
    ]

    operations = [
        migrations.AddField(
            model_name='myprofile',
            name='unban_date',
            field=models.DateField(blank=True, null=True, verbose_name='unban date'),
        ),
    ]
