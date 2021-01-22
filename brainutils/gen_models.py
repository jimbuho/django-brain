"""
The models module contains the classes available in the rendering of templates.

The available classes are:

* :class:`Models`: a list of models in a app. Each model in this listing uses the :ref:`Model` class.
* :class:`Model`: A wrapper of the app's Model class. It has methods that make it easier to get model fields.

@author: https://github.com/Nekmo/django-code-generator/tree/master/django_code_generator

"""
from django.db.models import ForeignKey
from django.db.models.fields import CharField, TextField, IntegerField, DateField, AutoField, BooleanField
from django.utils.text import camel_case_to_spaces

try:
    from django.db.models.loading import get_models
except ImportError:
    def get_models(app):
        """Get model classes from a AppConfig instance."""
        for model in app.get_models():
            yield model


#: CharField type fields. A CharField is string field with a limited size.
CHAR_FIELDS = (CharField,)
#: ForeignKey type fields. A ForeignKey is a one-to-many relationship.
FOREIGN_FIELDS = (ForeignKey,)
#: All fields that store text.
STRING_FIELDS = (CharField, TextField)
# Integer Fields
INTEGER_FIELDS = (IntegerField,)
#: All the fields used to filter.
FILTER_FIELDS = (CharField, IntegerField, DateField, AutoField, BooleanField)

NOT_FILTERABLE_FIELDS = ['creation_user','modification_user']
AUDITABLE_FIELDS = ['status','creation_date', 'modification_date'] + NOT_FILTERABLE_FIELDS
NO_INPUT_FIELDS = AUDITABLE_FIELDS + ['id','code']
SIMPLE_AUDITABLE_FIELDS = ['modification_date','modification_user']

LAST_FIELD = 'status'

def get_field_names(fields):
    """

    Fields name list ordered

    :param fields:
    :return:
    """
    fields_list = [x.name for x in fields]
    fields_list.sort(key=order_auditable_fields_at_end)
    return fields_list

def is_filterable_field(field):
    """

    Is a Filterable Field

    :param field:
    :return:
    """
    return (isinstance(field, FILTER_FIELDS) or isinstance(field, FOREIGN_FIELDS)) and \
           field.name not in NOT_FILTERABLE_FIELDS

def is_searchable_field(field):
    """

    Is a Searchable Field

    :param field:
    :return:
    """
    response = isinstance(field, FILTER_FIELDS) and field.name not in AUDITABLE_FIELDS
    return response

def is_inputable_field(field):
    """

    Check if field is not inputable field

    :param field:
    :return:
    """
    response = isinstance(field, FILTER_FIELDS) and field.name not in NO_INPUT_FIELDS
    return response

def is_audit_simple_field(field):
    """

    Auditable simple field

    :param field:
    :return:
    """
    response = field.name in SIMPLE_AUDITABLE_FIELDS
    return response

def is_string_field(field):
    """

    Check is string not auditable field

    :param field:
    :return:
    """
    response = isinstance(field, STRING_FIELDS) and field.name not in AUDITABLE_FIELDS
    return response

def order_auditable_fields_at_end(field):
    """

    Sort Condition for Auditable Fields

    :param field:
    :return:
    """
    if field in AUDITABLE_FIELDS:
        return 2 if field == LAST_FIELD else 1
    return 0

class Model:
    """A wrapper of the app's Model class. It has methods that make it easier to get model fields.

    This class receives a Model django db class.
    """
    def __init__(self, model):
        """
        :param django.db.models.Model model: a django Model class.
        """
        self.model = model

    @property
    def name(self):
        """Original model name. Just like the class."""
        return self.model._meta.object_name

    @property
    def field_names(self):
        """A list of all forward field names on the model and its parents,
        excluding ManyToManyFields.
        """
        return get_field_names(self.model._meta.fields)

    @property
    def local_field_names(self):
        """A list of field names on the model.
        """
        return get_field_names(self.model._meta.local_fields)

    @property
    def concrete_field_names(self):
        """A list of all concrete field names on the model and its parents."""
        return get_field_names(self.model._meta.concrete_fields)

    @property
    def string_field_names(self):
        """A list of concrete field names of type string (see :const:`STRING_FIELDS`)."""
        return get_field_names(filter(lambda x: is_string_field(x),
                                      self.model._meta.concrete_fields))

    @property
    def integer_field_names(self):
        """A list of concrete field names of type string (see :const:`INTEGER_FIELDS`)."""
        return get_field_names(filter(lambda x: isinstance(x, INTEGER_FIELDS),
                                      self.model._meta.concrete_fields))

    @property
    def foreign_field_names(self):
        """A list of concrete field names of type foreign key (see :const:`FOREIGN_FIELDS`)."""
        return get_field_names(filter(lambda x: isinstance(x, FOREIGN_FIELDS),
                                      self.model._meta.concrete_fields))

    @property
    def char_field_names(self):
        """A list of concrete field names of type char (see :const:`CHAR_FIELDS`)."""
        return get_field_names(filter(lambda x: is_searchable_field(x),
                                      self.model._meta.concrete_fields))

    @property
    def boolean_field_names(self):
        """A list of concrete field names of type boolean"""
        return get_field_names(filter(lambda x: isinstance(x, BooleanField),
                                      self.model._meta.concrete_fields))

    @property
    def filter_field_names(self):
        """A list of concrete field names used for filters (see :const:`FILTER_FIELDS`)."""
        return get_field_names(filter(lambda x: is_filterable_field(x),
                                      self.model._meta.concrete_fields))

    @property
    def input_fields(self):
        return get_field_names(filter(lambda x: is_inputable_field(x),
                                      self.model._meta.concrete_fields))

    @property
    def audit_fields(self):
        return get_field_names(filter(lambda x: is_audit_simple_field(x),
                                      self.model._meta.concrete_fields))

    @property
    def snake_case_name(self):
        """Model name in snake case."""
        return camel_case_to_spaces(self.name).replace(' ', '_')

    def __str__(self):
        return self.name


class Models(list):
    """A list of models in a app. Each model in this listing uses the
    :ref:`Model` class.

    This class receives an AppConfig instance.
    """
    def __init__(self, app):
        """
        :param AppConfig app: a django AppConfig instance.
        """
        super().__init__()
        self.app = app
        self.extend([Model(model) for model in get_models(self.app)])
