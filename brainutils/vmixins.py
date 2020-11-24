from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect


class LoginRequiredSecurityMixin:
    """

    Clase base para validar que el usuario este logueado

    """
    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        """

        Default dispath

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return super().dispatch(request, *args, **kwargs)

class SpecialSecurityMixin:
    """

    Clase base para revisar la seguridad de acceso a la vista que hereda
    de esta clase con un control especial.

    Se debe implementar en la clase que hereda:

    security_test(profile): Devuelve True/False
    get_fail_security_test_url(): Devuelve URL

    """

    def security_test(self, profile):
        """

        To Override

        :param profile:
        :return:
        """
        return profile is not None

    def get_fail_security_test_url(self, profile):
        """

        To Override

        :return:
        """
        return reverse('home')

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        """

        Valida si la condicion de seguridad no se cumple para redireccionar
        a la URL de fallo de seguridad

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        profile = self.request.user.customerprofile

        if not self.security_test(profile):
            return HttpResponseRedirect(redirect_to=self.get_fail_security_test_url(profile))

        return super().dispatch(request, *args, **kwargs)
