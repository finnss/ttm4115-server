# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-31 00:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_auto_20170331_0020'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sensor',
            name='description',
        ),
        migrations.AddField(
            model_name='sensor',
            name='monitoring_plant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='current_sensors', to='webapp.Plant'),
        ),
    ]
