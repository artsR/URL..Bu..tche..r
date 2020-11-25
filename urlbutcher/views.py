import random
import string

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import (
    HttpResponse, HttpResponseRedirect, HttpResponseForbidden, QueryDict
)
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from .forms import UrlForm
from .models import Url, FunnyQuote, SlugClickCounter
from .utils import (
    get_chuck_norris_fact, update_cookie_last_slugs, load_cookie_last_slugs
)



ALPHABET = string.ascii_letters + string.digits + '_- '
CHUCK_FACT_LEN_THRESHOLD = 100



@require_http_methods(['GET'])
def home(request):
    slug_id = request.session.pop('slug_id', None)

    if slug_id is None:
        form = UrlForm(user=request.user)
    else:
        uri = request.build_absolute_uri(slug_id)
        form = UrlForm(initial={'slug': uri})

    context = dict(form=form)

    last_slugs = load_cookie_last_slugs(request)
    if last_slugs is not None:
        context.update({'last_slugs': last_slugs})

    return render(request, 'home.html', context)


@login_required
def dashboard(request):
    user_slugs = request.user.url_set.all()

    context = dict(user_slugs=user_slugs)

    return render(request, 'dashboard.html', context)


@require_http_methods(['POST'])
def reset_cookie_last_slugs(request):
    response = redirect('urlbutcher:home')
    response.delete_cookie('slug_cookies')
    return response


"""from django.views.generic.base import RedirectView
class RedirectSlug(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        website = get_object_or_404(Url, pk=slug_id)

        slug_to_redirect = SlugClickCounter.objects.filter(pk=website).first()
        if slug_to_redirect is not None:
            slug_to_redirect.click_counter = F('click_counter') + 1
            slug_to_redirect.save()
        return super().get_redirect_url(url=website.url)

@require_http_methods(['GET'])
def redirect_slug(request, slug_id):
    website = get_object_or_404(Url, pk=slug_id)

    slug_to_redirect = SlugClickCounter.objects.filter(pk=website).first()
    if slug_to_redirect is not None:
        slug_to_redirect.click_counter = F('click_counter') + 1
        slug_to_redirect.save()

    return HttpResponseRedirect(website.url)


@require_http_methods(['POST'])
def create_short_slug(request):
    """Creates short `slug` for given URL using random characters."""
    form = UrlForm(request.POST, user=request.user)

    if form.is_valid():
        new_url = form.cleaned_data.get('url')
        custom_slug = form.cleaned_data.get('slug')

        new_slug = custom_slug if custom_slug else Url.get_unique_slug(ALPHABET)
        user = request.user if request.user.is_authenticated else None

        Url.objects.update_or_create(
            slug=new_slug,
            defaults={'url': new_url, 'created_at': timezone.now(), 'user': user}
        )
        request.session['slug_id'] = new_slug

        messages.success(
            request, 'Short link generated successfully. Copy and enjoy using it.'
        )
        messages.info(request, 'Your link can be used for at least 7 days.')

        recent_slugs = update_cookie_last_slugs(request, new_url, new_slug)
        response = redirect('urlbutcher:home')
        response.set_cookie(key='slug_cookies', value=recent_slugs)

        return response

    messages.error(request, 'Provided invalid data. Please try again')
    context = dict(form=form)

    return render(request, 'home.html', context)


@require_http_methods(['POST'])
def create_funny_slug(request):
    """Creates funny quotes as `slug` for given URL using database."""
    form = UrlForm(request.POST, user=request.user)
    form.fields['slug'].disabled = True

    if form.is_valid():
        new_url = form.cleaned_data.get('url')
        slug_quote = FunnyQuote.objects.random()
        new_slug = Url.get_unique_slug(
            ALPHABET, chars_to_draw=3, custom_slug=f'_{slug_quote}', separator='_'
        )
        user = request.user if request.user.is_authenticated else None

        Url.objects.update_or_create(
            slug=new_slug,
            defaults={'url': new_url, 'created_at': timezone.now(), 'user': user}
        )
        request.session['slug_id'] = new_slug

        messages.success(
            request, 'Short link generated successfully. Copy and enjoy using it.'
        )
        messages.info(request, 'Your link can be used for at least 7 days.')
        messages.info(request, f'Your slug: {new_slug}')

        recent_slugs = update_cookie_last_slugs(request, new_url, new_slug)
        response = redirect('urlbutcher:home')
        response.set_cookie(key='slug_cookies', value=recent_slugs)

        return response

    messages.error(request, 'Provided invalid data. Please try again')
    context = dict(form=form)

    return render(request, 'home.html', context)


@require_http_methods(['POST'])
def create_chuck_norris_slug(request):
    """Creates chuck norris fact as `slug` for given URL using external api."""
    form = UrlForm(request.POST, user=request.user)
    form.fields['slug'].disabled = True

    if form.is_valid():
        new_url = form.cleaned_data.get('url')
        slug_fact = get_chuck_norris_fact(CHUCK_FACT_LEN_THRESHOLD)
        new_slug = Url.get_unique_slug(
            ALPHABET, chars_to_draw=3, custom_slug=f'{slug_fact}', separator='__'
        )
        user = request.user if request.user.is_authenticated else None

        Url.objects.update_or_create(
            slug=new_slug,
            defaults={'url': new_url, 'created_at': timezone.now(), 'user': user}
        )
        request.session['slug_id'] = new_slug

        messages.success(
            request, 'Short link generated successfully. Copy and enjoy using it.'
        )
        messages.info(request, 'Your link can be used for at least 7 days.')
        messages.info(request, f'Your slug: {new_slug}')

        recent_slugs = update_cookie_last_slugs(request, new_url, new_slug)
        response = redirect('urlbutcher:home')
        response.set_cookie(key='slug_cookies', value=recent_slugs)

        return response

    messages.error(request, 'Provided invalid data. Please try again')
    context = dict(form=form)

    return render(request, 'home.html', context)


@login_required
def refresh_slug(request, slug_id):
    slug_obj = get_object_or_404(Url, pk=slug_id)
    if request.user != slug_obj.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        slug_obj.created_at = timezone.now()
        # Save and Let to know signals to not reset click counter:
        slug_obj.save(update_fields=['created_at'])

    return redirect('urlbutcher:dashboard')


@login_required
def edit_slug(request, slug_id):
    slug_obj = get_object_or_404(Url, pk=slug_id)
    if request.user != slug_obj.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = UrlForm(request.POST)
        if form.is_valid():
            slug_obj.url = form.cleaned_data['url']
            slug_obj.created_at = timezone.now()
            slug_obj.save()
            return redirect('urlbutcher:dashboard')
    else:
        form = UrlForm(initial={'slug': slug_obj.slug, 'url': slug_obj.url})
        form.fields['slug'].disabled = True

    context = dict(form=form)

    return render(request, 'edit_slug.html', context)


@login_required
def delete_slug(request, slug_id):
    slug_obj = get_object_or_404(Url, pk=slug_id)
    if request.user != slug_obj.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        slug_obj.delete()

    return redirect('urlbutcher:dashboard')
