# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-20 08:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0005_a_leave_attendance_daily_att_r_leave'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='emp_id',
        ),
        migrations.RemoveField(
            model_name='daily_att',
            name='emp_id',
        ),
        migrations.DeleteModel(
            name='attendance',
        ),
        migrations.DeleteModel(
            name='daily_att',
        ),
    ]
