from dotenv import load_dotenv

from .defaults import *

ENV_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(ENV_DIR, '.env'))

DEBUG=True

ALLOWED_HOSTS += ['127.0.0.1']

#DEBUG_COLLECTSTATIC = 1
