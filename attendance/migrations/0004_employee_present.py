# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-14 06:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0003_auto_20161214_0522'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='present',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
