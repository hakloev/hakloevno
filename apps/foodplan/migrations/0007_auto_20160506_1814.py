# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-06 16:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodplan', '0006_auto_20160506_0042'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dinnerplan',
            name='id',
        ),
        migrations.AlterField(
            model_name='dinnerplan',
            name='start_date',
            field=models.DateField(primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='dinnerplanitem',
            name='plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', related_query_name='item', to='foodplan.DinnerPlan'),
        ),
        migrations.AlterField(
            model_name='dinnerplanitem',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', related_query_name='recipe', to='foodplan.Recipe'),
        ),
    ]
