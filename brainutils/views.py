
from django.http import HttpResponseRedirect
from django.views.generic.base import View

from brainutils import messages

class LanguageChangeView(View):
    """

    Language Change View
    ===================

    Description
        Vista usada para cambiar el lenguaje del sistema

    """

    def get(self, request, *args, **kwargs):
        """

        Get

        Description
            Procesa el GET de esta vista

        :param args:
        :param kwargs:
        :return:
        """
        if 'name' in request.GET:
            messages.languages.change_language(request, request.GET.get('name'))

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
