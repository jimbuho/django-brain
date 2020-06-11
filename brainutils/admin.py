# -*- coding: utf-8 -*-
"""
.. module:: dbu-admin
   :platform: Unix, Windows
   :synopsis: Administrador de Modelos de modulo dbu

.. moduleauthor:: Diego Gonzalez <dgonzalez.jim@gmail.com>

"""
from __future__ import unicode_literals
from django.contrib import admin

from . import mixadmin
from . import models
from . import impexp

class LanguageAdmin(mixadmin.ModelAdminMixin):
    """

    Language Admin

    Description
        Administrador del modelo Language

    """
    list_display = ('id', 'name', 'default', 'modification_date', 'modification_user')

admin.site.register(models.Language, LanguageAdmin)

class MessageTraductionAdmin(mixadmin.ImportExportModelAdminMixin):
    """

    Message Traduction Admin

    Description
        Administrador del modelo MessageTraduction

    """
    resource_class = impexp.MessageTraductionResource
    list_display = ('id', 'language', 'message', 'modification_date', 'modification_user')

admin.site.register(models.MessageTraduction, MessageTraductionAdmin)

class MessageTraductionAdminTabular(admin.TabularInline):
    """

    Message Traduction Admin Tabular

    Description
        Administrador interno a Message para mostrar las traducciones de un
        mensaje en la misma pantalla.

    """
    model = models.MessageTraduction
    extra = 0
    max_num = 10
    exclude = ('status', 'creation_date', 'creation_user', 'modification_date', 'modification_user')

class MessageAdmin(mixadmin.ImportExportModelAdminMixin):
    """

    Message Admin

    Description
        Administrador del modelo Message, este contiene Message Traduction
        Admin Tabular.

    """
    inlines = [MessageTraductionAdminTabular, ]
    resource_class = impexp.MessageResource
    list_display = ('id', 'name', 'text', 'published', 'modification_date', 'modification_user')
    search_fields = ['name','text']
    list_filter = ['modification_date','creation_date']

admin.site.register(models.Message, MessageAdmin)

class ConfigurationAdmin(mixadmin.ImportExportModelAdminMixin):
    """

    Configuration Admin

    Description
        Administrador del modelo Configuration

    """
    resource_class = impexp.ConfigurationResource
    list_display = ('id', 'name', 'value', 'description', 'modification_date', 'modification_user')
    search_fields = ['name','value','description']

admin.site.register(models.Configuration, ConfigurationAdmin)
