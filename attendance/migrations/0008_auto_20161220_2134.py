# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-20 21:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0007_auto_20161220_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='r_leave',
            name='emp_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='attendance.employee'),
        ),
    ]