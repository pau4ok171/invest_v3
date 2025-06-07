from django.utils import translation


class DynamicLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check language in user session
        if hasattr(request, 'user') and request.user.is_authenticated:
            user_language = request.user.profile.locale
            translation.activate(user_language)
            request.LANGUAGE_CODE = user_language

        response = self.get_response(request)
        return response

