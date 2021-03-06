# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-04 14:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myprofile',
            name='favourite_snack',
        ),
        migrations.AddField(
            model_name='myprofile',
            name='birth_date',
            field=models.DateField(blank=True, null=True, verbose_name='birth date'),
        ),
        migrations.AddField(
            model_name='myprofile',
            name='first_name',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='first name'),
        ),
        migrations.AddField(
            model_name='myprofile',
            name='gender',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Male'), (2, 'Female')], null=True, verbose_name='gender'),
        ),
        migrations.AddField(
            model_name='myprofile',
            name='last_name',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='last name'),
        ),
    ]
