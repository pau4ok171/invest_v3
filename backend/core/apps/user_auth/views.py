from django.conf import settings
from django.contrib.auth.models import User

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.yandex.views import YandexOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from apps.user_auth.forms import UsernameVerificationForm


class CustomOAuth2Client(OAuth2Client):
    def __init__(
        self,
        request,
        consumer_key,
        consumer_secret,
        access_token_method,
        access_token_url,
        callback_url,
        _scope,  # This is fix for incompatibility between django-allauth==65.3.1 and dj-rest-auth==7.0.1
        scope_delimiter=" ",
        headers=None,
        basic_auth=False,
    ):
        super().__init__(
            request,
            consumer_key,
            consumer_secret,
            access_token_method,
            access_token_url,
            callback_url,
            scope_delimiter,
            headers,
            basic_auth,
        )


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_CALLBACK_URL
    client_class = CustomOAuth2Client


class YandexLogin(SocialLoginView):
    adapter_class = YandexOAuth2Adapter
    callback_url = settings.YANDEX_CALLBACK_URL
    client_class = CustomOAuth2Client


class GitHubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = settings.GITHUB_CALLBACK_URL
    client_class = CustomOAuth2Client


@extend_schema(
    methods=['GET'],
    summary='Check the availability of the username',
    description='Check if username is free',
    parameters=[
        OpenApiParameter(
            name='username',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=True,
            description='Username to be verified',
            examples=[
                OpenApiExample(
                    'Example 1',
                    value='johndoe',
                ),
            ]
        ),
    ],
    responses={
        200: OpenApiTypes.OBJECT,
        400: OpenApiTypes.OBJECT,
    },
    examples=[
        OpenApiExample(
            'Success Response',
            value={
                'isTaken': True,
                'message': 'The username is already taken',
            },
            status_codes=['200'],
        ),
        OpenApiExample(
            'Error Response',
            value={
                'errors': {
                    'username': ['The field is required'],
                }
            },
            status_codes=['400']
        ),
    ]
)
@api_view(['GET'])
def validate_username(request):
    form = UsernameVerificationForm(request.query_params)
    if form.is_valid():
        username = form.cleaned_data['username']
        is_taken = User.objects.filter(username__iexact=username).exists()
        message = "The username is already taken" if is_taken else "The username is free"
        return Response(data={
            "isTaken": is_taken,
            "message": message
        }, status=status.HTTP_200_OK)
    return Response(data={"errors": form.errors}, status=status.HTTP_400_BAD_REQUEST)

