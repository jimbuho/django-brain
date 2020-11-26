# -*- coding: utf-8 -*-
"""
.. module:: brainutils
   :platform: Unix, Windows
   :synopsis: URLS para modulo principal

.. moduleauthor:: Diego Gonzalez <dgonzalez.jim@gmail.com>

"""
from django.conf.urls import url

from . import views

urlpatterns = [

    # Standard Views
    url(r'^language/', views.LanguageChangeView.as_view(), name='language'),

]
