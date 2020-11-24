=====
Brain Utils
=====

Brain Utils is a Django app to let developers do not repeat same initial code for commons utilities. For example
configuration system values in database, configurable messages with traduction, stantard mixins for models and admins, etc.

Quick start
-----------

0. Install:

    git clone https://github.com/jimbuho/django-brain.git
    
    pip install -e django-brain-utils/

1. Add "brainutils" to your INSTALLED_APPS setting like this:

    INSTALLED_APPS = [
        ...
        'brainutils', # Before allauth
        ...
    ]

2. To start you can add a configurable message in your home page, example:

    {% load butils %}
    <h1>{% display_message request 'home.welcome' %}</h1>

3. Run ``python manage.py migrate`` to create the polls models.

4. Start the development server, visit http://127.0.0.1:8000 to watch first message and then go http://localhost:8000/admin/brainutils/message/
   to edit the created message, you may set there the message you want all times you need (to refressh changes you need
   to restart your webserver Apache, Nginx, etc). Is easy and you got a total control for each message and it traduction


More utilities
-----------

1. Configuration variables

You can set and use in your code a configuration variable very easy like this:

from brainutils import configuration

token = configuration.get_value('api.some.token','HEREYOURINITIALTOKENVALUE')
max_items_per_page = configuration.get_integer('commons.pagination.maxitems','10')

Then you may set a new value whenever you whant in http://localhost:8000/admin/brainutils/configuration/. Again you need
to restart your webserver to refresh changes

2. Model standart base fields:

from brainutils import mixins

class MyModel(mixins.AuditMixin):

    field1 = models.TextField(null=True, blank=True)
    field2 = models.TextField(null=True, blank=True)

Then you have this fields and you may use like you want:
creation_date, modification_date, creation_user, modification_user, status

3. Extra Models Administrator functionalities

If you need to interact with your model administrator with extra tags or actions you can use something like this:

class MyModelAdmin(mixadmin.ModelAdminMixin):

    list_display = ('field1', 'field2', 'modification_date', 'extra_actions')

    def myaction_view(self, request, id):
        try:

            obj = models.MyModel.objects.get(pk = id)

            success = obj.do_action()

            if success:
                return self.response_view(request, True, 'myaction_view', 'OK')
            else:
                return self.response_view(request, False, 'myaction_view', 'FAIL')
        except Exception as e:
            return self.response_view(request, False, 'myaction_view', str(e))

    def get_specific_dual_methods(self, obj):
        return [
            {'name':'actionname', 'activation':True, 'color':self.ENABLED_COLOR, 'myaction_view':self.myaction_view},
        ]

4. Language Manager

Youre application may needs to be multilanguage, theres an easy way with Brain Utils, just set in your code:

from brainutils import messages

def my_view(request):
    current_language = messages.languages.get_language(request)
    # Do whatever you want with language object
    # You may change the current language online in each moment if you need
    messages.languages.change_language(request,'english')

In templates:

{% for l in LANGUAGES %}
    {{l.title}}
{% endfor %}

Then you may set a new language value whenever you whant in http://localhost:8000/admin/brainutils/language/.

5. Customers Accounts

Brainutils gives you an standard login, signup and more functionalities for customers in your application.

To customize messages and else, copy our templates/account/ folder and change there whatever you want. You may
reuse a lot of funcionality inside there if your application web structure is similar. We use bootstrap as this:

<div class="main-container">
    <div class="inside-container">
        <!-- HERE PAGE CONTENT -->
    </div>
</div>
