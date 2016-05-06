# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-05 22:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodplan', '0005_auto_20160504_2112'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dinnerplan',
            options={'get_latest_by': 'end_date', 'ordering': ['-end_date'], 'verbose_name': 'Dinner Plan', 'verbose_name_plural': 'Dinner Plans'},
        ),
        migrations.AlterModelOptions(
            name='dinnerplanitem',
            options={'ordering': ['plan', 'day'], 'verbose_name': 'Dinner Plan Element', 'verbose_name_plural': 'Dinner Plan Elements'},
        ),
        migrations.RenameField(
            model_name='dinnerplanitem',
            old_name='period',
            new_name='plan',
        ),
        migrations.RemoveField(
            model_name='dinnerplan',
            name='meals',
        ),
        migrations.AlterField(
            model_name='dinnerplan',
            name='start_date',
            field=models.DateField(unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='dinnerplanitem',
            unique_together=set([('plan', 'day')]),
        ),
    ]
