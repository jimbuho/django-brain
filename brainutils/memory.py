# -*- coding: utf-8 -*-
"""
.. module:: dbu-memory
   :platform: Unix, Windows
   :synopsis: Helpers Principal de Memoria

.. moduleauthor:: Diego Gonzalez <dgonzalez.jim@gmail.com>

"""

class Memory:
    """

    Memory
    ===================

    Description
        Helper/Manager para mantener centralizado el registro
        en memoria cache.

    """
    MAIN = 'MAIN'

    MASTER_NAME = 'dbu.master.cache'

    def __init__(self):
        """

        INIT

        :return:
        """
        self.load()

    def load(self, step=None):
        """

        Load

        Description
            Inicializa el diccionario primario

        :return:
        """
        if not step:
            self.cache_dict = {}
            self.cache_dict[self.MAIN] = {}
        else:
            if not self.cache_dict:
                self.cache_dict = {}
            self.cache_dict[step] = {}

    def store(self, step, key, value, request):
        """

        Store

        Description
            Almacena en la clave de un paso del diccionario
            un nuevo valor.

        :param step:
        :param key:
        :param value:
        :param request:
        :return:
        """

        if not self.cache_dict or step not in self.cache_dict:
            self.load(step)

        if request:
            sd = self.cache_dict[step]
            sd[key] = value
            request.session[self.MASTER_NAME] = self.cache_dict
            request.session.modified = True

        self.show(request)

        return value

    def recover(self, step, key, request, sub_key=None, default_value=None):
        """

        Recover

        Description
            Recupera de la clave de un paso del diccionario
            un valor previamente almacenado.

        :param step:
        :param key:
        :param request:
        :return:
        """

        if request:
            self.cache_dict = request.session[self.MASTER_NAME] if self.MASTER_NAME in request.session else None

            if self.cache_dict and step in self.cache_dict and key in self.cache_dict[step]:
                if sub_key:
                    if sub_key in self.cache_dict[step][key]:
                        return self.cache_dict[step][key][sub_key]
                    return None
                else:
                    return self.cache_dict[step][key]
            elif default_value:
                return self.store(step, key, default_value, request)

        return None

    def update(self, step, key, sub_key, value, request):
        """

        Update

        Description
            Actualiza o agrega un valor en un sub-diccionario almacenado
            en el diccionario principal de la memoria cache.

        :param step:
        :param key:
        :param sub_key:
        :param value:
        :param request:
        :return:
        """
        subd_dict = None

        if request:
            if sub_key:
                subd_dict = self.recover(step, key, request)
                subd_dict = subd_dict if subd_dict else {}
                subd_dict[sub_key] = value
            else:
                subd_dict = value

            self.store(step, key, subd_dict, request)

        self.show(request)

        return subd_dict

    def clean(self, request, step=None, key=None, sub_key=None):
        """

        Clean

        Description
            Limpia de la memoria o del diccionario dependiendo de
            la clave o el paso dados. Si no son dados ninguno de
            ellos se limpia toda la sesion principal.

        :param step:
        :param key:
        :param request:
        :return:
        """

        if request:
            self.cache_dict = request.session[self.MASTER_NAME] if self.MASTER_NAME in request.session else None

            if self.cache_dict:
                if step and key and sub_key:
                    try:
                        del self.cache_dict[step][key][sub_key]
                        request.session[self.MASTER_NAME] = self.cache_dict
                    except:
                        print('[Memory.clean] No se puede limpiar la cache para (', step, key, sub_key, ')')
                elif step and key:
                    try:
                        del self.cache_dict[step][key]
                        request.session[self.MASTER_NAME] = self.cache_dict
                    except:
                        print('[Memory.clean] No se puede limpiar la cache para (', step, key, ')')
                elif step:
                    try:
                        del self.cache_dict[step]
                        request.session[self.MASTER_NAME] = self.cache_dict
                    except:
                        print('[Memory.clean] No se puede limpiar la cache para (', step, ')')
                else:
                    try:
                        del request.session[self.MASTER_NAME]
                    except:
                        print('[Memory.clean] No se puede limpiar la cache total.')
            else:
                print('[Memory.clean] No hay Cache Dict')

        self.show(request)

    def show(self, request):
        """

        Show

        Description
            Imprime el diccionario de la memoria

        :param request:
        :return:
        """

        if request:
            self.cache_dict = request.session[self.MASTER_NAME] if self.MASTER_NAME in request.session else None

            if self.cache_dict:
                print('[Memory.show] - CACHE:', self.cache_dict)
            else:
                print('[Memory.show]  Vacio', self.cache_dict)

cache = Memory()

class TopMemory(Memory):

    """

    Top Memory
    ===================

    Description
        Helper/Manager que funciona como especializacion de Memory
        para proceder con limpiezas de memoria escalares.

    """

    def clean_by_step(self, request, step):
        """

        Clean By Step

        Description
            Limpia la memoria por pasos, la limpieza des pasos iniciales
            hace que los posteriores pasos tambien sean limpiados.

        :param request:
        :param step:
        :return:
        """

        if step == self.MAIN:
            self.clean_main(request)

    def clean_main(self, request):
        """

        Clean Step 0

        Description
            Limpieza paso 0 (HOME)

        :param request:
        :return:
        """
        self.clean(request, self.MAIN)

top = TopMemory()