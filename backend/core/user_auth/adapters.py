from urllib.parse import urljoin

from allauth.account.adapter import DefaultAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        url = f'auth/verify-email/{emailconfirmation.key}'
        return urljoin("http://localhost:5173", url)

    def send_password_reset_mail(self, user, email, context):
        return self.send_mail("account/email/password_reset_key", email, context)
