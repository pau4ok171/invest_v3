from datetime import timedelta

from decouple import config as env_conf
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from pathlib import Path

######################################################################
# General
######################################################################
BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = env_conf('DJANGO_KEY')

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

ASGI_APPLICATION = 'config.asgi.application'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SITE_ID = int(env_conf('SITE_ID'))

######################################################################
# Domains
######################################################################
FRONTENT_DOMAIN = 'http://localhost:5173'

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:8000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8000",
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Security settings
SECURE_CROSS_ORIGIN_OPENER_POLICY = None

######################################################################
# Apps
######################################################################
INSTALLED_APPS = [
    # UNFOLD
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',
    'unfold.contrib.inlines',
    'unfold.contrib.import_export',
    'parler',
    'daphne',

    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',

    # External apps
    'channels',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'drf_spectacular',

    # Auth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.headless',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.yandex',
    'allauth.socialaccount.providers.github',

    # DRF Auth
    'dj_rest_auth',
    'dj_rest_auth.registration',

    # SimpleJWT
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',

    # Other
    'django_celery_beat',
    'django_celery_results',
    'django_cleanup.apps.CleanupConfig',
    'import_export',

    # My apps
    'apps.invest.apps.InvestConfig',
    'apps.portfolio.apps.PortfolioConfig',
    'apps.notes.apps.NotesConfig',
    'apps.statements.apps.StatementsConfig',
    'apps.news.apps.NewsConfig',
    'apps.analysis.apps.AnalysisConfig',
    'apps.site_admin.apps.AdminConfig',
    'apps.user_profile.apps.UserProfileConfig',
    'apps.user_auth.apps.UserAuthConfig',
]

######################################################################
# Middleware
######################################################################
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'i18n.middleware.DynamicLanguageMiddleware',
    'django.middleware.locale.LocaleMiddleware',

    'allauth.account.middleware.AccountMiddleware'
]

######################################################################
# Templates
######################################################################
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

######################################################################
# Channels
######################################################################
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    }
}

######################################################################
# Password Validation
######################################################################
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

######################################################################
# Email
######################################################################
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = env_conf('EMAIL_HOST')
EMAIL_HOST_USER = env_conf('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env_conf('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587

######################################################################
# Authentication
######################################################################
# All auth
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']
ACCOUNT_LOGIN_METHODS = {'username', 'email'}
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_CONFIRMATION_HMAC = False
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_ADAPTER = "apps.user_auth.adapters.CustomAccountAdapter"
SOCIALACCOUNT_EMAIL_AUTHENTICATION = True
SOCIALACCOUNT_AUTO_SIGNUP = True

# Google OAuth2
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': (
            'profile',
            'email',
        ),
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'FETCH_USERINFO': True,
        'OAUTH_PKCE_ENABLED': True,
    }
}

GOOGLE_CALLBACK_URL = 'http://127.0.0.1:8000/accounts/google/login/callback/'
YANDEX_CALLBACK_URL = 'http://127.0.0.1:8000/accounts/yandex/login/callback/'
GITHUB_CALLBACK_URL = 'http://localhost:5173/auth/github/login/callback/'

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=6),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=15),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": "HS256",
    "SIGNING_KEY": env_conf('DJANGO_KEY'),
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(hours=6),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=15),

    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}

# Rest auth
PASSWORD_RESET_URL = f'{FRONTENT_DOMAIN}/auth/new-password/<uid64>/<token>'
REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_COOKIE': 'jwt-auth',
    'JWT_AUTH_REFRESH_COOKIE': 'jwt-refresh',
    'JWT_AUTH_HTTPONLY': True,
    'SESSION_LOGIN': False,
    'OLD_PASSWORD_FIELD_ENABLED': True,
    'LOGOUT_ON_PASSWORD_CHANGE': True,

    'LOGIN_SERIALIZER': 'dj_rest_auth.serializers.LoginSerializer',
    'TOKEN_SERIALIZER': 'dj_rest_auth.serializers.TokenSerializer',
    'JWT_SERIALIZER': 'dj_rest_auth.serializers.JWTSerializer',
    'JWT_SERIALIZER_WITH_EXPIRATION': 'dj_rest_auth.serializers.JWTSerializerWithExpiration',
    'JWT_TOKEN_CLAIMS_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenObtainPairSerializer',
    'USER_DETAILS_SERIALIZER': 'apps.user_profile.serializers.UserProfileSerializer',
    'PASSWORD_RESET_SERIALIZER': 'apps.user_auth.serializers.CustomPasswordResetSerializer',
    'PASSWORD_RESET_CONFIRM_SERIALIZER': 'dj_rest_auth.serializers.PasswordResetConfirmSerializer',
    'PASSWORD_CHANGE_SERIALIZER': 'dj_rest_auth.serializers.PasswordChangeSerializer',

    'REGISTER_SERIALIZER': 'dj_rest_auth.registration.serializers.RegisterSerializer',

    'REGISTER_PERMISSION_CLASSES': ('rest_framework.permissions.AllowAny',),

    'TOKEN_MODEL': 'rest_framework.authtoken.models.Token',
    'TOKEN_CREATOR': 'dj_rest_auth.utils.default_create_token',

    'PASSWORD_RESET_USE_SITES_DOMAIN': True,

    'JWT_AUTH_REFRESH_COOKIE_PATH': '/',
    'JWT_AUTH_SECURE': False,
    'JWT_AUTH_SAMESITE': 'Lax',
    'JWT_AUTH_RETURN_EXPIRATION': False,
    'JWT_AUTH_COOKIE_USE_CSRF': False,
    'JWT_AUTH_COOKIE_ENFORCE_CSRF_ON_UNAUTHENTICATED': False,
}

######################################################################
# Celery
######################################################################
CELERY_BROKER_URL = env_conf('CELERY_BROKER_URL')
CELERY_TASK_TRACK_STARTED = True  # запускает трекинг задач Celery

# Планировщик задач
CELERY_BEAT_SCHEDULER = \
    'django_celery_beat.schedulers:DatabaseScheduler'  # Celery настроен на использование планировщика из базы данных

CELERY_BROKER_TRANSPORT_OPTION = {'visibility_timeout': 3600}  # время ожидания видимости 1 час
CELERY_RESULT_BACKEND = 'django-db'  # указание для django_celery_results куда записывать результат выполнения задач
CELERY_ACCEPT_CONTENT = ['application/json']  # это тип содержимого, разрешенный к получению
CELERY_TASK_SERIALIZER = 'json'  # это строка, используемая для определения метода сериализации по умолчанию
CELERY_RESULT_SERIALIZER = 'json'  # является типом формата сериализации результатов

CELERY_TASK_DEFAULT_QUEUE = 'default'  # celery будет использовать это имя очереди
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

######################################################################
# Rest Framework
######################################################################
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

}

######################################################################
# Django Spectacular
######################################################################
SPECTACULAR_SETTINGS = {
    'TITLE': 'Finargo API Project',
    'DESCRIPTION': 'API for Finargo site',
    'VERSION': '1.0.0',
}

######################################################################
# Localization
######################################################################
LANGUAGE_CODE = 'en'
LANGUAGES = [
    ('en', 'English'),
    ('ru', 'Русский'),
    ('fr', 'Français'),
    ('es', 'Español'),
    ('de', 'Deutsch'),
    ('pl', 'Polski'),
    ('it', 'Italiano'),
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

PARLER_DEFAULT_LANGUAGE_CODE = 'en'

PARLER_LANGUAGES = {
    int(env_conf('SITE_ID')): (
        {'code': 'en', },
        {'code': 'ru', },
        {'code': 'fr', },
        {'code': 'es', },
        {'code': 'de', },
        {'code': 'pl', },
        {'code': 'it', },
    ),
    'default': {
        'fallbacks': ['en'],  # defaults to PARLER_DEFAULT_LANGUAGE_CODE
        'hide_untranslated': False,  # the default; let .active_translations() return fallbacks too.
    }
}

######################################################################
# Static
######################################################################
STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = 'media/'

MEDIA_ROOT = BASE_DIR / 'media'

######################################################################
# Unfold
######################################################################
UNFOLD = {
    "SHOW_HISTORY": True,  # show/hide "History" button, default: True
    "SHOW_LANGUAGES": True,
    "ENVIRONMENT": "config.settings.utils.environment_callback",
    "SHOW_VIEW_ON_SITE": True,  # show/hide "View on site" button, default: True
    "SHOW_BACK_BUTTON": False,  # show/hide "Back" button on changeform in header, default: False
    "BORDER_RADIUS": "8px",
    "COLORS": {
        "base": {
            "50": "249, 250, 251",
            "100": "243, 244, 246",
            "200": "229, 231, 235",
            "300": "209, 213, 219",
            "400": "156, 163, 175",
            "500": "107, 114, 128",
            "600": "75, 85, 99",
            "700": "55, 65, 81",
            "800": "31, 41, 55",
            "900": "17, 24, 39",
            "950": "3, 7, 18",
        },
        "primary": {
            "50": "250, 245, 255",
            "100": "243, 232, 255",
            "200": "233, 213, 255",
            "300": "216, 180, 254",
            "400": "33, 145, 235",
            "500": "33, 145, 235",
            "600": "33, 145, 235",
            "700": "126, 34, 206",
            "800": "107, 33, 168",
            "900": "88, 28, 135",
            "950": "59, 7, 100",
        },
        "font": {
            "subtle-light": "var(--color-base-500)",  # text-base-500
            "subtle-dark": "var(--color-base-400)",  # text-base-400
            "default-light": "var(--color-base-600)",  # text-base-600
            "default-dark": "var(--color-base-300)",  # text-base-300
            "important-light": "var(--color-base-900)",  # text-base-900
            "important-dark": "var(--color-base-100)",  # text-base-100
        },
    },
    "EXTENSIONS": {
        "language_selector": True,  # Включите переключатель языков
    },
    "SIDEBAR": {
        "show_search": True,  # Search in applications and models names
        "show_all_applications": True,  # Dropdown with all applications and models
        "navigation": [
            {
                "title": _('Analysis'),
                "collapsible": True,
                "items": [
                    {
                        "title": _('Analysis'),
                        "icon": 'network_intelligence',
                        'link': reverse_lazy(
                            "admin:analysis_companyanalysis_changelist",
                        ),
                    }
                ],
            },
            {
                "title": _('Celery results'),
                "collapsible": True,
                "items": [
                    {
                        "title": _('Group Results'),
                        "icon": 'sports_score',
                        'link': reverse_lazy(
                            "admin:django_celery_results_groupresult_changelist",
                        ),
                    },
                    {
                        "title": _('Task results'),
                        "icon": 'sports_score',
                        'link': reverse_lazy(
                            "admin:django_celery_results_taskresult_changelist"
                        ),
                    },
                ],
            },
            {
                "title": _('Invest'),
                "collapsible": True,
                "items": [
                    {
                        "title": _('Analyst ideas'),
                        "icon": 'online_prediction',
                        "link": reverse_lazy(
                            "admin:invest_analystidea_changelist"
                        ),
                    },
                    {
                        "title": _('Analysts'),
                        "icon": 'groups_3',
                        "link": reverse_lazy(
                            "admin:invest_analyst_changelist"
                        ),
                    },
                    {
                        "title": _('Candles per day'),
                        "icon": 'candlestick_chart',
                        "link": reverse_lazy(
                            "admin:invest_candleperday_changelist"
                        ),
                    },
                    {
                        "title": _('Companies'),
                        "icon": 'apartment',
                        "link": reverse_lazy(
                            "admin:invest_company_changelist"
                        ),
                    },
                    {
                        "title": _('Countries'),
                        "icon": 'public',
                        "link": reverse_lazy(
                            "admin:invest_country_changelist"
                        ),
                    },
                    {
                        "title": _('Currencies'),
                        "icon": 'euro_symbol',
                        "link": reverse_lazy(
                            "admin:invest_currency_changelist"
                        ),
                    },
                    {
                        "title": _('Dividends'),
                        "icon": 'confirmation_number',
                        "link": reverse_lazy(
                            "admin:invest_dividend_changelist"
                        ),
                    },
                    {
                        "title": _('Industries'),
                        "icon": 'precision_manufacturing',
                        "link": reverse_lazy(
                            "admin:invest_industry_changelist"
                        ),
                    },
                    {
                        "title": _('Markets'),
                        "icon": 'api',
                        "link": reverse_lazy(
                            "admin:invest_market_changelist"
                        ),
                    },
                    {
                        "title": _('Reports metadata'),
                        "icon": 'browse_activity',
                        "link": reverse_lazy(
                            "admin:invest_reportmetadata_changelist"
                        ),
                    },
                    {
                        "title": _('Sectors'),
                        "icon": 'factory',
                        "link": reverse_lazy(
                            "admin:invest_sector_changelist"
                        ),
                    },
                ],
            },
            {
                "title": _('News'),
                "collapsible": True,
                "items": [
                    {
                        "title": _('News'),
                        "icon": 'newspaper',
                        'link': reverse_lazy(
                            "admin:news_news_changelist"
                        ),
                    },
                ],
            },
            {
                "title": _('Notes'),
                "collapsible": True,
                "items": [
                    {
                        "title": _('Notes'),
                        "icon": 'draw',
                        "link": reverse_lazy(
                            "admin:notes_note_changelist"
                        ),
                    },
                ],
            },
            {
                "title": _('Portfolios'),
                "collapsible": True,
                "items": [
                    {
                        "title": _('Portfolios Companies'),
                        "icon": 'work_update',
                        "link": reverse_lazy(
                            "admin:portfolio_portfoliocompany_changelist"
                        ),
                    },
                    {
                        "title": _('Portfolios'),
                        "icon": 'enterprise',
                        "link": reverse_lazy(
                            "admin:portfolio_portfolio_changelist"
                        ),
                    },
                ],
            },
            {
                "title": _('Statements'),
                "collapsible": True,
                "items": [
                    {
                        "title": _('Statements'),
                        "icon": 'search_check_2',
                        'link': reverse_lazy(
                            "admin:statements_statement_changelist"
                        ),
                    },
                ],
            },
            {
                "title": _('User Profiles'),
                "collapsible": True,
                "items": [
                    {
                        "title": _('Profiles'),
                        "icon": 'badge',
                        "link": reverse_lazy(
                            "admin:user_profile_profile_changelist"
                        ),
                    },
                ],
            },
            {
                "title": _('Token Blacklists'),
                "collapsible": True,
                "items": [
                    {
                        "title": _('Blacklisted Tokens'),
                        "icon": '',
                        "link": reverse_lazy(
                            "admin:token_blacklist_blacklistedtoken_changelist"
                        ),
                    },
                    {
                        "title": _('Outstanding Tokens'),
                        "icon": '',
                        "link": reverse_lazy(
                            "admin:token_blacklist_outstandingtoken_changelist"
                        ),
                    },
                ],
            },
            {
                "title": _('Accounts'),
                "collapsible": True,
                "items": [
                    {
                        "title": _('Email Addresses'),
                        "icon": '',
                        "link": reverse_lazy(
                            "admin:account_emailaddress_changelist"
                        ),
                    },
                    {
                        "title": _('Email Confirmations'),
                        "icon": '',
                        "link": reverse_lazy(
                            "admin:account_emailconfirmation_changelist"
                        ),
                    },
                ],
            },
            {
                "title": _('Social Accounts'),
                "collapsible": True,
                "items": [
                    {
                        "title": _('Social Accounts'),
                        "icon": '',
                        "link": reverse_lazy(
                            "admin:socialaccount_socialaccount_changelist"
                        ),
                    },
                    {
                        "title": _('Social Apps'),
                        "icon": '',
                        "link": reverse_lazy(
                            "admin:socialaccount_socialapp_changelist"
                        ),
                    },
                    {
                        "title": _('Social Tokens'),
                        "icon": '',
                        "link": reverse_lazy(
                            "admin:socialaccount_socialtoken_changelist"
                        ),
                    },
                ],
            },
            {
                "title": _('Sites'),
                "collapsible": True,
                "items": [
                    {
                        "title": _('Sites'),
                        "icon": '',
                        "link": reverse_lazy(
                            "admin:sites_site_changelist"
                        ),
                    },
                ],
            },
            {
                "title": _("Celery Tasks"),
                "collapsible": True,
                "items": [
                    {
                        "title": _("Clocked"),
                        "icon": "hourglass_bottom",
                        "link": reverse_lazy(
                            "admin:django_celery_beat_clockedschedule_changelist"
                        ),
                    },
                    {
                        "title": _("Crontabs"),
                        "icon": "update",
                        "link": reverse_lazy(
                            "admin:django_celery_beat_crontabschedule_changelist"
                        ),
                    },
                    {
                        "title": _("Intervals"),
                        "icon": "timer",
                        "link": reverse_lazy(
                            "admin:django_celery_beat_intervalschedule_changelist"
                        ),
                    },
                    {
                        "title": _("Periodic tasks"),
                        "icon": "task",
                        "link": reverse_lazy(
                            "admin:django_celery_beat_periodictask_changelist"
                        ),
                    },
                    {
                        "title": _("Solar events"),
                        "icon": "event",
                        "link": reverse_lazy(
                            "admin:django_celery_beat_solarschedule_changelist"
                        ),
                    },
                ],
            },
            {
                "title": _('Users & Groups'),
                "collapsible": True,
                "items": [
                    {
                        "title": _("Users"),
                        "icon": "account_circle",
                        "link": reverse_lazy("admin:auth_user_changelist"),
                    },
                    {
                        "title": _("Groups"),
                        "icon": "group",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                ],
            },
            {
                "title": _('Auth Tokens'),
                "collapsible": True,
                "items": [
                    {
                        "title": _("Token"),
                        "icon": 'password',
                        "link": reverse_lazy("admin:authtoken_tokenproxy_changelist"),
                    },
                ],
            },
        ],
    },
}
