import os
from datetime import timedelta
from dotenv import load_dotenv

ENV_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(ENV_DIR, '.env'))

from .defaults import *


DEBUG=True

ALLOWED_HOSTS += ['127.0.0.1', 'localhost']

INSTALLED_APPS += [
    'rest_framework',
    'api',
]

#DEBUG_COLLECTSTATIC = 1

# Token Authenticaton
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=10),

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=15),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}
