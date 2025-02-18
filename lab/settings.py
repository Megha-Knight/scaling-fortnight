from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Now use them in settings.py
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "arunprakashcoc@gmail.com"  # Replace with your email
EMAIL_HOST_PASSWORD = "ztce dgaw mofi qyky"  # Use environment variables for security
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

