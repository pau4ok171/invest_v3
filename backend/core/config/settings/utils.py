from django.conf import settings

from django.utils.translation import gettext_lazy as _


def environment_callback(request):
    if settings.DEBUG:
        return [_("Development"), "primary"]

    return [_("Production"), "primary"]
