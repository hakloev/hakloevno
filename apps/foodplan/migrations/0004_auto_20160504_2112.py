# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-04 19:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodplan', '0003_dinnerplanitem_eaten'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dinnerplan',
            name='cost',
            field=models.FloatField(blank=True, default=0.0, null=True, verbose_name='Total cost'),
        ),
    ]