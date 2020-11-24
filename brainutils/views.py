from django.views.generic.base import TemplateView

class TermsView(TemplateView):
    """

    Terms View
    ===================

    Description
        Vista usada para mostrar los terminos y condiciones

    """
    template_name = "brainutils/terms.html"
