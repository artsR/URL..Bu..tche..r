import random
import string

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from django.views.decorators.http import require_http_methods

from .models import Url, FunnyQuote
from .forms import UrlForm
from .utils import get_chuck_norris_fact, update_cookie_last_slugs


ALPHABET = string.ascii_letters + string.digits + '_- '
CHUCK_FACT_LEN_THRESHOLD = 100

# Create your views here.

@require_http_methods(['GET'])
def home(request):
    slug_id = request.session.pop('slug_id', None)

    if slug_id is None:
        form = UrlForm()
    else:
        hostname = request.META
        form = UrlForm(initial={'slug': f'{hostname}/{slug_id}'})

    context = dict(form=form)

    return render(request, 'home.html', context)


