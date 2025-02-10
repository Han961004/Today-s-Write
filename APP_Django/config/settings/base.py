from pathlib import Path
from datetime import timedelta
import os
import sentry_sdk


sentry_sdk.init(
    dsn="https://e18fe28da6bfa15d5871fa25f8ba140c@o4508765361537024.ingest.us.sentry.io/4508765366845440",
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    _experiments={
        # Set continuous_profiling_auto_start to True
        # to automatically start the profiler on when
        # possible.
        "continuous_profiling_auto_start": True,
    },
)

APPEND_SLASH = False  # URL 끝에 슬래시를 붙이지 않도록 설정
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-+&2r64c8n7j&xc=q1x=@dt3kiq!8=_y&5ux$li+(0ndw_r$=5$'

INSTALLED_APPS = [
    # apps
    'apps.accounts.apps.AccountsConfig',
    # 'apps.posts.apps.PostsConfig',
    # 'apps.comments.apps.CommentsConfig',
    
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Requirements
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_yasg',
    
    
    'django_prometheus',
    

]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # JWT 인증
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=12),  # 액세스 토큰 만료 시간 (12시간)
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),   # 리프레시 토큰 만료 시간 (7일)
    'ROTATE_REFRESH_TOKENS': True,                # 새로고침 시 리프레시 토큰 갱신
    'BLACKLIST_AFTER_ROTATION': True,             # 사용된 리프레시 토큰을 블랙리스트에 추가
}

AUTH_USER_MODEL = 'accounts.User'
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    'corsheaders.middleware.CorsMiddleware',
        
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware",

]

ROOT_URLCONF = 'config.urls'

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

ASGI_APPLICATION = 'config.asgi.application'  # 비동기
WSGI_APPLICATION = 'config.wsgi.application'

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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
