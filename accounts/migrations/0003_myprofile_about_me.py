# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-04 14:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20171104_1531'),
    ]

    operations = [
        migrations.AddField(
            model_name='myprofile',
            name='about_me',
            field=models.TextField(blank=True, verbose_name='about me'),
        ),
    ]