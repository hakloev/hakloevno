# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-19 19:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodplan', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='rating',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Not rated'), (1, 'Awful'), (2, 'Bad'), (3, 'Average'), (4, 'Good'), (5, 'Great'), (6, 'Superb')], default=0),
        ),
    ]
