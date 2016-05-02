# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-02 21:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('url', models.URLField()),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Recipe',
                'ordering': ['title'],
                'verbose_name_plural': 'Recipes',
            },
        ),
        migrations.CreateModel(
            name='WeekPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='WeekPlanRecipes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.IntegerField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')])),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodplan.Recipe')),
                ('week', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodplan.WeekPlan')),
            ],
            options={
                'verbose_name': 'Plan',
                'ordering': ['day'],
                'verbose_name_plural': 'Plans',
            },
        ),
        migrations.AlterUniqueTogether(
            name='weekplanrecipes',
            unique_together=set([('week', 'recipe', 'day')]),
        ),
    ]
