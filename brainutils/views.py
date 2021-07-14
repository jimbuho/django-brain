
from django.http import HttpResponseRedirect
from django.views.generic.base import View

from brainutils import messages

from . import signals

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
            resp, lang = messages.languages.change_language(request, request.GET.get('name'))
            
            if resp:
                signals.language_changed.send(sender=self.__class__, user=request.user, language=lang)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
