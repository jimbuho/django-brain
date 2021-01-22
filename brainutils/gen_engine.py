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

    def __init__(self, app_name, template_name, ext='py', mode=None):
        """

        Construye la app

        :param app_name:
        """
        self.app_name = app_name

        self.template_name = template_name

        self.ext = ext

        self.mode = mode

        installed_apps = dict(get_apps())

        self.app = installed_apps.get(app_name)

        if self.app is None:
            raise Exception('App {} is not available'.format(app_name))

    def render(self):
        """

        Renderiza el template dado en el archivo solicitado

        :return:
        """

        if self.ext == 'py':
            to_path = os.path.join(self.app.path, '%s.py' % self.template_name)
            rendered = render_to_string('code/%s_template.html' % self.template_name,
                                        {'models': gen_models.Models(self.app), 'app': self.app})

            with open(to_path, 'w') as f:
                f.write(rendered)
        else: # html
            models = gen_models.Models(self.app)

            for model in models:

                path = os.path.join(self.app.path, 'templates', self.app.name)

                try:
                    os.mkdir(path)
                except:
                    pass

                if self.template_name == 'delete':
                    file_name = '%s_delete_confirm.html' % str(model.name).lower()
                else:
                    file_name = '%s_%s.html' % (self.template_name, str(model.name).lower())

                to_path = os.path.join(path, file_name)

                rendered = render_to_string('code/%s_html_template.html' % self.template_name,
                                            {'model': model, 'app': self.app, 'mode': self.mode})

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

class CRUDGenerator:

    """

    Generador de CRUD Clases para una App

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
        Template(self.app_name, 'forms').render()
        print('<== Success Generated FORMS for', self.app_name)
        Template(self.app_name, 'urls').render()
        print('<== Success Generated URLS for', self.app_name)
        Template(self.app_name, 'views').render()
        print('<== Success Generated VIEWS for', self.app_name)

        print('<== Success Generated [all CRUD] for', self.app_name)

class CRUDHTMLGenerator:

    """

    Generador de CRUD HTML para una App

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
        list_mode = str(input('Choice a list template mode: [A] Table, [B] Article:'))
        list_mode = list_mode.upper() if list_mode else None
        list_mode = 'article' if list_mode and list_mode == 'B' else 'table'

        Template(self.app_name, 'create', 'html').render()
        print('<== Success Generated CREATE HTML for', self.app_name)
        Template(self.app_name, 'update', 'html').render()
        print('<== Success Generated UPDATE HTML for', self.app_name)
        Template(self.app_name, 'list', 'html', list_mode).render()
        print('<== Success Generated LIST HTML for', self.app_name)
        Template(self.app_name, 'delete', 'html').render()
        print('<== Success Generated DELETE HTML for', self.app_name)

        print('<== Success Generated [all CRUD HTML] for', self.app_name)

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

        elif option == 'crud':

            if app_name:
                CRUDGenerator(app_name).generate()
            else:
                apps = get_apps()

                for k,v in apps:

                    if DJANGO_APPS_PREFIX not in k:

                        yes_not = str(input('Do you want to generate code for app %s? '
                                            '(This gonna replace your code if exists: views, forms and urls) [y/N]:' % k))

                        if yes_not == 'y':
                            CRUDGenerator(k).generate()
        elif option == 'crud_html':

            if app_name:
                CRUDHTMLGenerator(app_name).generate()
            else:
                apps = get_apps()

                for k,v in apps:

                    if DJANGO_APPS_PREFIX not in k:

                        yes_not = str(input('Do you want to generate html for app %s? '
                                            '(This gonna replace your code if exists: update, create, list, delete) [y/N]:' % k))

                        if yes_not == 'y':
                            CRUDHTMLGenerator(k).generate()