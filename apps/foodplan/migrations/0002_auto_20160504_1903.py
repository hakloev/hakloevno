# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-04 17:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodplan', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dinnerplanitem',
            options={'ordering': ['period', 'day'], 'verbose_name': 'Dinner Plan Element', 'verbose_name_plural': 'Dinner Plan Elements'},
        ),
    ]
