import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'your-secret-key-here'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'django.contrib.sites',  # Django Allauth に必要
    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
    # 'allauth.socialaccount.providers.twitter',  # 必要なプロバイダーを追加
    'lyrics',
    'accounts',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'allauth.account.middleware.AccountMiddleware',  # 追加する行
]

ROOT_URLCONF = 'Voice_Training_ClientSide.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 'allauth.account.context_processors.account',  # 追加する行
                # 'allauth.socialaccount.context_processors.socialaccount',  # 追加する行
            ],
        },
    },
]

WSGI_APPLICATION = 'Voice_Training_ClientSide.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'lyrics/static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # 本番環境用の静的ファイル収集ディレクトリ

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django Allauth 設定
# Django Allauth 設定
LOGIN_REDIRECT_URL = '/lyrics/input/'  # ログイン後のリダイレクト先
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'  # ユーザー名とメールアドレスで認証
ACCOUNT_EMAIL_REQUIRED = True  # メールアドレス必須
ACCOUNT_EMAIL_VERIFICATION = 'optional'  # メールアドレスの確認を任意
ACCOUNT_USERNAME_REQUIRED = True  # ユーザー名必須
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True  # パスワード確認欄
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True  # メール確認後にログイン
# AUTHENTICATION_BACKENDS = (
#     'django.contrib.auth.backends.ModelBackend',
#     'allauth.account.auth_backends.AuthenticationBackend',
    
# )

# SITE_ID = 1

LOGIN_REDIRECT_URL = '/lyrics/input/'  # ログイン後のリダイレクト先
LOGOUT_REDIRECT_URL = '/accounts/login/'  # ログアウト後のリダイレクト先

# ソーシャルアカウントのプロバイダーの設定
# SOCIALACCOUNT_PROVIDERS = {
#     'twitter': {
#         'APP': {
#             'client_id': '<your-client-id>',
#             'secret': '<your-client-secret>',
#             'key': '<your-api-key>'
#         }
#     }
# }
