# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-20 21:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0004_employee_present'),
    ]

    operations = [
        migrations.CreateModel(
            name='r_leave',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date1', models.DateField()),
                ('date2', models.DateField()),
                ('l_type', models.CharField(max_length=10)),
                ('reason', models.CharField(max_length=100)),
                ('emp_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.employee')),
            ],
        ),
    ]