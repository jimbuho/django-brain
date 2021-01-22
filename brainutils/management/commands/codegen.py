# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

import traceback

from brainutils import gen_engine

class ConsoleCommand:
    """

    Console Main Code Generator

    """

    def __init__(self):

        self.generator = gen_engine.GeneratorEngine()

    def menu(self):
        """

        Menu

        Description
            Despliega el Menu

        :return:
        """
        print('BRAIN UTILS GENERATOR')
        print('What we gonna do?:')
        print('1. Generate Admins')
        print('2. Generate CRUD URL-Views-Forms')
        print('3. Generate Signup - Login')
        print('4. Generate CRUD HML (Beta)')
        print('0. Exit')
        print('***************************')

    def welcome(self):
        print('_________________________\n')
        print('Welcome to Brain Utils')
        print('_________________________\n')

    def main(self):
        """

        MAIN

        Description
            Funcion principal de entrada

        :return:
        """
        self.welcome()

        self.menu()

        try:
            while (True):
                option = str(input("Select and option[and press ENTER]: "))
                if option == '0':
                    break
                elif option == '1':
                    self.option_1()
                    self.menu()
                elif option == '2':
                    self.option_2()
                    self.menu()
                elif option == '3':
                    self.option_3()
                    self.menu()
                elif option == '4':
                    self.option_4()
                    self.menu()
                else:
                    print('Invalid Option:', option)
        except Exception as e:
            print('Error to process: %s' % str(e))
            traceback.print_exc()

    def option_1(self):
        try:
            app_name = str(input('Input the app name (empty if you need for all):'))

            if not app_name or app_name == '':
                self.generator.run('admin')
            else:
                self.generator.run('admin', app_name)
        except Exception as e:
            print('Error al procesar opcion 1:', str(e))
            traceback.print_exc()

    def option_2(self):
        try:
            app_name = str(input('Input the app name (empty if you need for all):'))

            if not app_name or app_name == '':
                self.generator.run('crud')
            else:
                self.generator.run('crud', app_name)
        except Exception as e:
            print('Error al procesar opcion 2:', str(e))
            traceback.print_exc()

    def option_3(self):
        print('In Work...')

    def option_4(self):
        try:
            app_name = str(input('Input the app name:'))
            if app_name:
                self.generator.run('crud_html', app_name)
        except Exception as e:
            print('Error al procesar opcion 2:', str(e))
            traceback.print_exc()

class Command(BaseCommand):
    """

    Comandos de configuracion

    """
    args = '<app app ...>'
    help = 'Console Code  Generator'

    def handle(self, *args, **kwargs):
        """

        Generador de codigo por consola

        :param args:
        :param options:
        :return:
        """
        ConsoleCommand().main()


