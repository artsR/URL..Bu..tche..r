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
        uri = request.build_absolute_uri(slug_id)
        form = UrlForm(initial={'slug': uri})

    context = dict(form=form)

    return render(request, 'home.html', context)


@require_http_methods(['GET'])
def redirect_slug(request, slug_id):
    website = get_object_or_404(Url, pk=slug_id)
    return HttpResponseRedirect(website.url)


@require_http_methods(['POST'])
def create_short_slug(request):
    """Creates short `slug` for given URL using random characters."""
    form = UrlForm(request.POST)

    if form.is_valid():
        new_url = form.cleaned_data.get('url')
        custom_slug = form.cleaned_data.get('slug')

        new_slug = custom_slug if custom_slug else Url.get_unique_slug(ALPHABET)

        Url.objects.update_or_create(
            slug=new_slug,
            defaults={'url': new_url, 'created_at': timezone.now()}
        )
        request.session['slug_id'] = new_slug

        messages.success(
            request, 'Short link generated successfully. Copy and enjoy using it.'
        )
        messages.info(request, 'Your link can be used for at least 7 days.')

        return redirect('home')

    messages.error(request, 'Provided invalid data. Please try again')
    context = dict(form=form)

    return render(request, 'home.html', context)


@require_http_methods(['POST'])
def create_funny_slug(request):
    """Creates funny quotes as `slug` for given URL using database."""
    form = UrlForm(request.POST)
    form.fields['slug'].disabled = True

    if form.is_valid():
        new_url = form.cleaned_data.get('url')
        slug_quote = FunnyQuote.objects.random()
        new_slug = Url.get_unique_slug(
            ALPHABET, k=3, custom_slug=f'_{slug_quote}', sep='_'
        )

        Url.objects.update_or_create(
            slug=new_slug,
            defaults={'url': new_url, 'created_at': timezone.now()}
        )
        request.session['slug_id'] = new_slug

        messages.success(
            request, 'Short link generated successfully. Copy and enjoy using it.'
        )
        messages.info(request, 'Your link can be used for at least 7 days.')
        messages.info(request, f'Your slug: {new_slug}')

        return redirect('home')

    messages.error(request, 'Provided invalid data. Please try again')
    context = dict(form=form)

    return render(request, 'home.html', context)


@require_http_methods(['POST'])
def create_chuck_norris_slug(request):
    """Creates chuck norris fact as `slug` for given URL using external api."""
    form = UrlForm(request.POST)
    form.fields['slug'].disabled = True

    if form.is_valid():
        new_url = form.cleaned_data.get('url')
        slug_fact = get_chuck_norris_fact(CHUCK_FACT_LEN_THRESHOLD)
        new_slug = Url.get_unique_slug(
            ALPHABET, k=3, custom_slug=f'{slug_fact}', sep='__'
        )

        Url.objects.update_or_create(
            slug=new_slug,
            defaults={'url': new_url, 'created_at': timezone.now()}
        )
        request.session['slug_id'] = new_slug

        messages.success(
            request, 'Short link generated successfully. Copy and enjoy using it.'
        )
        messages.info(request, 'Your link can be used for at least 7 days.')
        messages.info(request, f'Your slug: {new_slug}')

        return redirect('home')

    messages.error(request, 'Provided invalid data. Please try again')
    context = dict(form=form)

    return render(request, 'home.html', context)
