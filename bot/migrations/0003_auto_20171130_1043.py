# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-30 10:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_auto_20171129_1327'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='errorlog',
            name='transaction',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='server',
        ),
        migrations.DeleteModel(
            name='Errorlog',
        ),
        migrations.DeleteModel(
            name='Server',
        ),
    ]