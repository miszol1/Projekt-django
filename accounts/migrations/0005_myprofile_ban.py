# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-28 17:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20171104_1850'),
    ]

    operations = [
        migrations.AddField(
            model_name='myprofile',
            name='ban',
            field=models.PositiveSmallIntegerField(choices=[(False, b'False'), (True, b'True')], default=False, verbose_name='ban'),
            preserve_default=False,
        ),
    ]
