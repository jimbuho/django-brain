# -*- coding: utf-8 -*-
"""
.. module:: main
   :platform: Unix, Windows
   :synopsis: Mixins de uso principal y comun

.. moduleauthor:: Diego Gonzalez <dgonzalez.jim@gmail.com>

"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from . import properties

import traceback
import uuid

class CommonManager(models.Manager):
    """

    Common Manager
    ===================

    Description
        Esta clase permite manejar un manager comun para todos los modelos
        que extiendan de Audit Mixin y extraer consultas comunes.

    """

    def get_active(self, *args, **kwargs):
        """

        Get Active

        """
        filtered = self.get_queryset().filter(*args, **kwargs)
        filtered = filtered.filter(status=AuditMixin.ACTIVE)
        return filtered

    def get_enabled(self, *args, **kwargs):
        """

        Get Enabled

        """
        try:
            elements = self.get_queryset().filter(*args, **kwargs).filter(status=AuditMixin.ACTIVE)
            if elements.count() > 0:
                return elements[0]
        except Exception as e:
            traceback.print_exc()

        return None

class AuditMixin(models.Model):
    """

    Audit Mixin
    ===================

    Description
        Esta clase permite manejar un modelos con campos comunes
        usados para auditoria y control de existencia.

    """

    ACTIVE = properties.ACTIVE
    INACTIVE = properties.INACTIVE

    ESTADO_CHOICES = (
        (ACTIVE, 'Activo'),
        (INACTIVE, 'Inactivo'),
    )

    status = models.CharField(max_length=1, choices=ESTADO_CHOICES, default=ACTIVE)
    creation_user = models.CharField(max_length=64, null=True, blank=True)
    modification_user = models.CharField(max_length=64, null=True, blank=True)
    creation_date = models.DateTimeField(null=True, blank=True)
    modification_date = models.DateTimeField(null=True, blank=True)

    objects = CommonManager()

    def __init__(self, *args, **kwargs):
        """

        INIT

        :param args:
        :param kwargs:
        :return:
        """
        self.username = None
        super(AuditMixin, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        """

        Save

        Description
            Save Overload

        :param args:
        :param kwargs:
        :return:
        """
        user = self.username

        if not self.pk:
            self.status = self.ACTIVE

        if not self.pk:

            if not self.creation_user and user:
                if isinstance(user, User): user = user.username
                if user: self.creation_user = user[:64]

        if not self.creation_date:
            self.creation_date = timezone.now()

        self.modification_date = timezone.now()
        if user:
            if isinstance(user, User): user = user.username
            self.modification_user = user[:64]

        obj = super(AuditMixin, self).save(*args, **kwargs)
        return obj

    def is_enabled(self):
        """

        Is Enabled

        Description
            Reg is Available

        :return:
        """
        return self.status == self.ACTIVE

    def disable(self, user=None):
        """

        Disable

        Description
            Disable a reg

        :param user:
        :return:
        """
        self.status = self.INACTIVE
        self.modification_user = user[:64] if user else ''
        self.save()

    def enable(self, user=None):
        """

        Enable

        Description
            Enable a reg

        :param user:
        :return:
        """
        self.status = self.ACTIVE
        self.modification_user = user[:64] if user else ''
        self.save()

    def get_creation_date(self):
        """

        Get Creation Time

        Description
            Get Creation Time Formated

        :return:
        """
        try:
            return self.creation_date.strftime('%d/%m/%Y %H:%M:%S')
        except:
            return str(self.creation_date)

    def get_modification_date(self):
        """

        Get Modification Time

        Description
            Get Modification Time Formated

        :return:
        """
        try:
            return self.modification_date.strftime('%d/%m/%Y %H:%M:%S')
        except:
            return str(self.modification_date)

    @staticmethod
    def get_unique_code():
        """

        Get Unique Code

        Description
            Metodo estatico para generar codigos Unicos

        :return:
        """
        uid = uuid.uuid4().int & (1<<64)-1
        return str(uid)[:12]

    def generate_unique_id_12(self):
        """

        Generates Unique ID 12

        Description
            Generates a Unique ID of 12 digits

        :return:
        """
        return AuditMixin.get_unique_code()

    class Meta:
        abstract = True
