# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-27 20:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=200, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='blogentry',
            name='tags',
            field=models.ManyToManyField(to='blog.Tag'),
        ),
    ]
