# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-28 18:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_myprofile_ban'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myprofile',
            name='ban',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(False, b'False'), (True, b'True')], null=True, verbose_name='ban'),
        ),
    ]
