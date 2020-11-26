import os

from django.template.loader import render_to_string

from django.apps import apps

from . import gen_models

DJANGO_APPS_PREFIX = 'django.contrib'

def get_apps():
    """

    Get All Apps in Context

    :return:
    """
    for app_config in apps.get_app_configs():
        yield app_config.name, app_config

class Template:
    """

    Template Render

    """

    def __init__(self, app_name, template_name):
        """

        Construye la app

        :param app_name:
        """
        self.app_name = app_name

        self.template_name = template_name

        installed_apps = dict(get_apps())

        self.app = installed_apps.get(app_name)

        if self.app is None:
            raise Exception('App {} is not available'.format(app_name))

    def render(self):
        """

        Renderiza el template dado en el archivo solicitado

        :return:
        """

        to_path = os.path.join(self.app.path, '%s.py' % self.template_name)

        rendered = render_to_string('code/%s_template.html' % self.template_name,
                                    {'models': gen_models.Models(self.app), 'app': self.app})

        with open(to_path, 'w') as f:
            f.write(rendered)

class AdminGenerator:

    """

    Generadir de Admin Clases para una App

    """

    def __init__(self, app_name):
        """

        Constructor

        :param app_name:
        """
        self.app_name = app_name

    def generate(self):
        """

        Construye admin

        :return:
        """
        Template(self.app_name, 'admin').render()
        print('<== Success Generated [Admins] for', self.app_name)


class GeneratorEngine:
    """

    Motor de Generacion

    """

    def run(self, option, app_name=None):
        """

        Generador de Codigo para una app y del tipo dado por option

        :param option:
        :param app_name:
        :return:
        """

        if option == 'admin':

            if app_name:
                AdminGenerator(app_name).generate()
            else:
                apps = get_apps()

                for k,v in apps:

                    if DJANGO_APPS_PREFIX not in k:

                        yes_not = str(input('Do you want to generate code for app %s? '
                                            '(This gonna replace your code if exists) [y/N]:' % k))

                        if yes_not == 'y':
                            AdminGenerator(k).generate()
