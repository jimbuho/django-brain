# -*- coding: utf-8 -*-
"""
.. module:: dbu-messages
   :platform: Unix, Windows
   :synopsis: Manejador de mensajes de uso comun y principal

.. moduleauthor:: Diego Gonzalez <dgonzalez.jim@gmail.com>

"""
from . import models
from . import memory

class LanguageManager:
    """

    Language Manager
    ===================

    Description
        Manejador de lenguajes, permite conseguir el lenguaje principal del sistema.

    """

    def get_default(self):
        """

        Get Default

        Description
            Permite consultar el lenguaje por defecto del sistema, si hay mas de uno
            devuelve el primero en localizarse

        :return
            models.Language -- El lenguaje principal del sistema

        """
        main_languages = models.Language.objects.get_active(default=True)

        if main_languages.exists():
            return main_languages.first().name

        name = 'spanish'

        models.Language.objects.create(
            name=name,
            title='Espanol',
            i18n='es',
            default=True
        )

        return name

    def get_by_name(self, name):
        """

        Get By Name

        Description
            Consulta un lenguaje por su nombre

        :return
            models.Language -- El lenguaje

        """
        main_languages = models.Language.objects.get_active(name=name)

        if main_languages.count() > 0:
            return main_languages.first()

        return None

    def get_language(self, request):
        """
        Get Default

        Description
            Permite obtener el lenguaje actualmente elegido en el sistema, lo obtiene
            de sesion. Si no esta en sesion aun, se toma el lenguaje por defecto y se lo
            registra en la sesion para una futura ocacion.

        :return
            models.Language -- El lenguaje principal del sistema

        """
        if request:
            return memory.cache.recover(memory.Memory.MAIN, 'dbu.languages.current', request,
                                        default_value=self.get_default())

        return self.get_default()


    def get_language_object(self, request):
        """
        Get Default

        Description
            Permite obtener el modelo lenguaje actualmente elegido en el sistema, lo obtiene
            de sesion. Si no esta en sesion aun, se toma el lenguaje por defecto y se lo
            registra en la sesion para una futura ocacion.

        :return
            String -- Abreviacion i18n

        """
        lang_name = self.get_language(request)
        languages = models.Language.objects.get_active(name = lang_name)

        if languages.exists():
            return languages.first()
        else:
            return self.create_language(lang_name)

    def change_language(self, request, name):
        """
        Change Language

        Description
            Permite realizar el cambio de lenguaje al indicado por el parametro 'name'

        :return
            Boolean -- True si el cambio fue realizado, False en caso contrario

        """
        languages = models.Language.objects.get_active(name = name)

        if languages.count() > 0:
            first = languages.first()
            memory.cache.store(memory.Memory.MAIN, 'dbu.languages.current', first.name, request)
            return True, first

        return False, None

    def create_language(self, name):
        """

        Create Language

        Description
            Crea lenguaje por defecto

        :param name:

        """
        try:
            return models.Language.objects.create(name = name, title = name)
        except Exception as e:
            languages = models.Language.objects.get_active(name = name)
            if languages.count() > 0:
                return languages.first()

            return None

languages = LanguageManager()

class MessageManager:
    """

    Messages Manager
    ===================

    Description
        Manejador de mensajes, mantiene en sesion los mensajes
        que ya fueron consultados, ademas permite internacionalizacion
        de los mismos.

    """

    DEFAULT_MSG = '-NO MESSAGE AVAILABLE-'

    def __init__(self, language=None):
        self.language = language

        if self.language:
            if self.language == languages.get_default():
                self.is_default = True
            else:
                self.is_default = False
        else:
            self.is_default = True

    def get_message(self, name, default=None):
        """

        Get Message

        Description
            Permite consultar un mensaje por su nombre, devuelve incluida
            su internacionalizacion, si no existe devuelve un mensaje por
            defecto y crea dicho mensaje. Almacena en memoria de servidor.

        :return
            String -- El texto del mensaje

        """
        message = name #self.DEFAULT_MSG

        if self.is_default:
            language_name = 'default'
        else:
            language_name = self.language

        if hasattr(get_message, 'messages'):
            messages_dict = get_message.messages
        else:
            messages_dict = {}

        if '%s.%s' % (language_name, name) in messages_dict:
            message = messages_dict['%s.%s' % (language_name, name)]
        else:
            try:
                if self.is_default:
                    messages = models.Message.objects.get_active(name = name, published=True)
                else:
                    messages = models.MessageTraduction.objects.get_active(message__name = name,
                                                                           language__name = self.language)

                if messages.count() > 0:
                    message = messages.first().text
                    messages_dict['%s.%s' % (language_name, name)] = message
                    get_message.messages = messages_dict
                else:
                    self.create_default(name, self.language, default)
            except Exception as e:
                print('[brainutils-messages] Error al obtener el mensaje: %s' % str(e))
                message = None

        if message == self.DEFAULT_MSG:
            return name
        return message

    def create_default(self, name, language, default=None):
        """

        Create Default

        Description
            Permite crear un mensaje por defecto en caso de que no exista,
            asi estara disponible para que el administrador simplemente
            llene el texto correspondiente y sus traducciones.

        """
        try:
            if name is None or len(name) > 100:
                return
            else:
                if self.is_default:
                    models.Message.objects.create(name=name, text=default if default else name) #self.DEFAULT_MSG
                else:
                    try:
                        message = models.Message.objects.get(name = name)
                    except models.Message.DoesNotExist:
                        message = models.Message.objects.create(name=name, text=default if default else name)

                    models.MessageTraduction.objects.create(message=message, text=default if default else name,
                                                            language=languages.get_by_name(language))
        except Exception as e:
            import traceback
            traceback.print_exc()

def get_message(name, language=None, default=None):
    """

    Get Message

    Description
        Acceso rapido a los mensajes

    :param name: El nombre unico del mensaje
    :param language: El lenguaje del mensaje
    :return: String -- El texto del mensaje
    """
    return MessageManager(language).get_message(name, default=default)

def get_full_message(request, name, default=None):
    """

    Get Message Complete

    Description
        Acceso rapido a los mensajes con internacionalizacion

    :param request:
    :param name: El nombre unico del mensaje
    :return: String -- El texto del mensaje
    """
    return MessageManager(languages.get_language(request)).get_message(name, default=default)

def format_message(message, *args):
    """
    
    Format message

    Description
        Agrega variables a un mensaje
    
    :param message:
    :param *args: Lista de valores a reempazarse en el mensaje
    :return message: Mensaje evaluado
    """
    if not args:
        return message

    for index, option in enumerate(args):
        message = message.replace('{%d}' % index, option)

    return message
