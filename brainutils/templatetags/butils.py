# -*- coding: utf-8 -*-
"""
.. module:: dbu-maintags
   :platform: Unix, Windows
   :synopsis: Tags del modulo DBU

.. moduleauthor:: Diego Gonzalez <dgonzalez.jim@gmail.com>

"""
from django import template
from django.utils.safestring import mark_safe

from brainutils import messages

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
