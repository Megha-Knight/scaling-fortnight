from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# settings.py
RAZORPAY_KEY_ID = 'rzp_test_eC0LeZT3x01zFb' # Replace with your Razorpay key ID
RAZORPAY_KEY_SECRET = 'kFWo7vcD7pSYhoDv2bNwy1CV'  # Replace with your Razorpay secret key
RAZORPAY_CURRENCY = "INR"
# Security settings
SECRET_KEY = "django-insecure-4rsmnieyhqv79&z6899%pw!3u3_h)+vh0dy#6qx7(du=_d@10("
DEBUG = True
ALLOWED_HOSTS = []
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'lab',  # Make sure your app is listed here
]




MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "idea.urls"

# settings.py

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "idea.wsgi.application"

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'idealab',  # Replace with your actual database name
        'USER': 'root',       # Replace with your MySQL username
        'PASSWORD': 'arun',   # Replace with your MySQL password
        'HOST': 'localhost',           # Assuming MySQL is running locally
        'PORT': '3306',               # Default MySQL port
    }
}

# Email configuration
# Configure admin and sender email addresses
ADMIN_EMAIL = "harrismahendran18@gmail.com"
DEFAULT_FROM_EMAIL = "arunprakashcoc@gmail.com"

# SMTP settings for sending emails
# settings.py

# Email backend configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # Using SMTP to send emails
EMAIL_HOST = 'smtp.gmail.com'  # Gmail SMTP server
EMAIL_PORT = 587  # Use port 587 for TLS
EMAIL_USE_TLS = True  # Enable TLS for secure connection

# Your sender email credentials
EMAIL_HOST_USER = 'arunprakashcoc@gmail.com'  # The email you are sending from
EMAIL_HOST_PASSWORD = 'ztce dgaw mofi qyky'  # Your Gmail App password or Gmail password (if 2FA is not enabled)

# Default sender email
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER  # This will be the sender email used in all outgoing emails

# Admin email to receive notifications
ADMIN_EMAIL = 'harrismahendran18@gmail.com'  # The admin email to which notifications will be sent

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# settings.py

AUTH_USER_MODEL = 'lab.CustomUser'

# Localization settings
LANGUAGE_CODE = "en-us"
TIME_ZONE =  'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"

import os

# Media files settings
MEDIA_URL = '/media/'  # URL for serving media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Directory to store uploaded media files

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
