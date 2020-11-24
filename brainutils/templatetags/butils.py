# -*- coding: utf-8 -*-
"""
.. module:: dbu-maintags
   :platform: Unix, Windows
   :synopsis: Tags del modulo DBU

.. moduleauthor:: Diego Gonzalez <dgonzalez.jim@gmail.com>

"""
from django import template
from django.utils.safestring import mark_safe

from brainutils import messages, configuration

register = template.Library()

@register.simple_tag
def display_message(request, name):
    """

    Display

    Description
        Tag para mostrar un mensaje previamente almacenado en BDD
        y memoria, en pantalla formateado en HTML

    :param request: Request Actual
    :param name: Nombre del Mensaje
    :return: String -- Mensaje HTML

    """
    language = messages.languages.get_language(request)
    return mark_safe( messages.get_message(name, language) )

@register.simple_tag
def display_configuration(name, default=None):
    """

    Display

    Description
        Tag para mostrar una configuracion previamente almacenada en BDD
        y memoria, en pantalla formateado en HTML

    :param name: Nombre de la configuracion
    :param default: Valor por defecto
    :return: String -- Mensaje HTML

    """
    return mark_safe( configuration.get_value(name, default) )
