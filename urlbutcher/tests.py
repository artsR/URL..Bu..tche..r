import random
import string
from datetime import timedelta

from django.test import TestCase, SimpleTestCase
from django.utils import timezone
from django.urls import reverse
from django.core.exceptions import ValidationError

from .models import Url, FunnyQuote, EXPIRES_IN
from .forms import UrlForm

# Create your tests here.



def create_db_entry(cls, **kwargs):
    entry = cls(**kwargs)
    entry.save()
    return entry


class HomePagesTest(SimpleTestCase):
    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')


class SlugPagesTest(TestCase):
    def setUp(self):
        self.valid_url = 'http://www.example.pl/example-example/example'
        self.unique_slug = 'tEsT'
        self.expired_slug = 'aBcD'
        self.recent_slug = 'xYz'
        self.expired_date = timezone.now() + timedelta(days=-EXPIRES_IN)
        self.recent_date = timezone.now()
        create_db_entry(
            Url, slug=self.expired_slug, url=self.valid_url, created_at=self.expired_date
        )
        create_db_entry(
            Url, slug=self.recent_slug, url=self.valid_url, created_at=self.recent_date
        )

    def test_slug_short_page_status_code(self):
        response = self.client.post(reverse('create_short_slug'))
        self.assertEqual(response.status_code, 200)

    def test_slug_funny_page_status_code(self):
        response = self.client.post(reverse('create_funny_slug'))
        self.assertEqual(response.status_code, 200)

    def test_slug_chuck_page_status_code(self):
        response = self.client.post(reverse('create_chuck_slug'))
        self.assertEqual(response.status_code, 200)

    def test_create_short_slug_with_custom_unique_slug(self):
        """Creates entry in Url with short slug provided by user.
        There is no conflict with slugs already created.
        """
        data = {'slug': self.unique_slug, 'url': self.valid_url}
        response = self.client.post(reverse('create_short_slug'), data)
        self.assertEqual(response.status_code, 302)
        # Retrieve created object from db:
        posted_slug = Url.objects.get(slug=self.unique_slug)
        self.assertEqual(posted_slug.url, self.valid_url)

    def test_create_short_slug_with_custome_expired_slug(self):
        """Creates entry in Url with short slug provided by user.
        There is  conflict with slug already created but because of expiration
        it will be overwritten.
        """
        data = {'slug': self.expired_slug, 'url': self.valid_url}
        response = self.client.post(reverse('create_short_slug'), data)
        self.assertEqual(response.status_code, 302)
        # Retrieve updated object:
        posted_slug = Url.objects.get(slug=self.expired_slug)
        self.assertNotEqual(posted_slug.created_at, self.expired_date)

    def test_create_short_slug_with_custom_duplicate_slug(self):
        """Creates entry in Url with short slug provided by user.
        There is conflict with slugs already created - entry will not be created.
        """
        data = {'slug': self.recent_slug, 'url': self.valid_url}
        response = self.client.post(reverse('create_short_slug'), data)
        self.assertEqual(response.status_code, 200)
        posted_slug = Url.objects.get(slug=self.recent_slug)
        self.assertEqual(posted_slug.created_at, self.recent_date)

    def test_create_funny_slug_without_custom_slug(self):
        pass

    def test_create_funny_slug_with_invalid_custom_slug(self):
        pass

    def test_create_chuck_slug_without_custom_slug(self):
        pass

    def test_create_chuck_slug_with_invalid_custom_slug(self):
        pass


class AccountsPagesTest(SimpleTestCase):
    def test_accounts_login_page_status_code_for_anonymous(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_accounts_register_page_status_code_for_anonymous(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_accounts_logout_page_status_code_for_anonymous(self):
        response = self.client.get(reverse('logout'), follow=True)
        self.assertRedirects(response, '/', 302, 200)
        self.assertTemplateUsed(response, 'home.html')



class UrlModelTest(TestCase):
    def test_expired_with_old_slug(self):
        """Url.expired() returns True for entries
        that was created EXPIRES_IN days ago and more.
        """
        expired_date = timezone.now() + timedelta(days=-EXPIRES_IN)
        expired_entry = create_db_entry(
            Url, slug='test', url='http://www.example.pl', created_at=expired_date
        )
        self.assertIs(expired_entry.expired(), True)


    def test_expired_with_recent_slug(self):
        """Url.expired() returns False for entries
        that was created less than EXPIRES_IN days ago.
        """
        non_expired_date = timezone.now() + timedelta(days=-EXPIRES_IN+1)
        non_expired_entry = create_db_entry(
            Url, slug='test', url='http://www.example.pl', created_at=non_expired_date
        )
        self.assertIs(non_expired_entry.expired(), False)


    def test_get_unique_slug_for_multi_drawing(self):
        """get_unique_slug() draws new slug till slug is unique.
        Drawing population has length of number of attempts to get unique slug.
        """
        no_of_entries = 5
        POPULATION = string.ascii_letters[:no_of_entries]
        sample_slugs = list()
        url = 'http://www.example.pl'
        for i in range(no_of_entries):
            random_slug = Url.get_unique_slug(POPULATION, k=1)
            entry = create_db_entry(Url, slug=random_slug, url=url)
            sample_slugs.append(random_slug)

        # At this point sample should equal population
        self.assertIs(len(sample_slugs), len(POPULATION))

        # Sample should also have the same items as population
        self.assertEqual(set(sample_slugs), set(POPULATION))


    def test_get_unique_slug_for_expired_slug(self):
        """get_unique_slug() returns drawn slug that already exists in db
        but is expired as valid slug that can be used.
        """
        POPULATION = string.ascii_letters
        max_slug_len = 3
        url = 'http://www.example.pl'

        random.seed(100)
        random_slug = ''.join(random.choices(POPULATION, k=max_slug_len))
        expired_date = timezone.now() + timedelta(days=-EXPIRES_IN)
        expired_entry = create_db_entry(
            Url, slug=random_slug, url=url, created_at=expired_date
        )

        random.seed(100)
        new_slug = Url.get_unique_slug(POPULATION, k=max_slug_len)

        self.assertEqual(new_slug, expired_entry.slug)



class UrlFormTest(TestCase):
    def setUp(self):
        self.valid_url = 'http://www.example.pl'
        self.empty_slug = ''
        self.valid_slug = 'aBcD'

    def test_clean_slug_for_empty(self):
        """clean_slug() returns empty string for empty slug field in form."""
        form = UrlForm(data={'url': self.valid_url, 'slug': self.empty_slug})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['slug'], '')

    def test_clean_slug_for_unique_slug(self):
        """clean_slug() returns the same value for unique slug field in form."""
        form = UrlForm(data={'url': self.valid_url, 'slug': self.valid_slug})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['slug'], self.valid_slug)

    def test_clean_slug_for_duplicate_slug(self):
        """clean_slug() raise ValidationError for slug field value in form that
        already exists in database.
        """
        create_db_entry(Url, url=self.valid_url, slug=self.valid_slug)
        slug_already_in_db = self.valid_slug
        form = UrlForm(data={'url':self.valid_url, 'slug': slug_already_in_db})
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('slug', code='already_used'))
