from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm

from dj_rest_auth.serializers import PasswordResetSerializer

from user_auth.forms import CustomAllAuthPasswordResetForm

# Get the UserModel
UserModel = get_user_model()


class CustomPasswordResetSerializer(PasswordResetSerializer):
    @property
    def password_reset_form_class(self):
        if 'allauth' in settings.INSTALLED_APPS:
            return CustomAllAuthPasswordResetForm
        else:
            return PasswordResetForm
