from dotenv import load_dotenv

from .defaults import *


load_dotenv('.env')

DEBUG=True

ALLOWED_HOSTS += ['127.0.0.1']

#SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']
