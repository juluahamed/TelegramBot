# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from bot.models import Transaction, Server, Errorlog

admin.site.register(Transaction)
admin.site.register(Server)
admin.site.register(Errorlog)

