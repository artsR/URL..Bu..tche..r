import re
import requests
import json
from requests.exceptions import HTTPError

from django.http import Http404



def get_chuck_norris_fact(threshold):
    """Get random fact about Chuck Norris no longer than `threshold`."""
    url = 'https://api.chucknorris.io/jokes/random'
    cleaned_fact = None
    while cleaned_fact is None:
        response = requests.get(url)

        try:
            response.raise_for_status()
        except HTTPError:
            raise Http404('External API not found')

        fact_json = response.json()
        fact_raw = fact_json.get('value')
        fact, len_fact = clean_chuck_norris_fact(fact_raw)
        cleaned_fact = fact if len_fact < threshold else None

    return cleaned_fact


def clean_chuck_norris_fact(fact):
    """Converts fact using CamelCase like style,
    replacing special characters with under/dunder score.
    """
    replacement = [
        (f'[\']', ' '),
        (r'[,"]', '_'),
        (r'[^a-zA-Z0-9_\- ]+', '__')
    ]
    for _from, _to in replacement:
        fact = re.sub(_from, _to, fact)

    cleaned_fact = ''.join(word.title() for word in fact.split())

    return cleaned_fact, len(cleaned_fact)


def update_cookie_last_slugs(request, url, slug):
    slug_cookies = request.COOKIES.get('slug_cookies', json.dumps(list()))
    try:
        slug_history = json.loads(slug_cookies)
        slug_history.extend(
            (url, f"http://{request.META['HTTP_HOST']}/{slug}")
        )
    except TypeError:
        pass
    except SyntaxError:
        slug_history = list()
        pass
    return json.dumps(slug_history[-4:])


