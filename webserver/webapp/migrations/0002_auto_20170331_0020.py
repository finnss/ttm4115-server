# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-31 00:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
