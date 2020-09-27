import random
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone



EXPIRES_IN = 7



class Url(models.Model):
    slug = models.CharField(max_length=150, primary_key=True)
    url = models.URLField(max_length=512)
    created_at = models.DateTimeField(default=timezone.now, blank=True)

    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    def expired(self):
        return self.created_at + timedelta(days=EXPIRES_IN) < timezone.now()

    def __str__(self):
        return f'{self.url}\n{self.slug}'

    @classmethod
    def get_unique_slug(cls, alphabet, *, chars_to_draw=6, custom_slug='', separator=''):
        """Generates unique slug. Ready to save into database.

        Args:
            alphabet: Population of characters to draw
            chars_to_draw: Number of characters to draw
            custom_slug: Suffix slug eg. funny quote
            separator: Seperator between random prefix and custom suffix
        """
        #TODO: add some kind of timeout...
        while True:
            slug_id = ''.join(
                char for char in random.choices(alphabet, k=chars_to_draw) if char != ' '
            )
            slug_id = f'{slug_id}{separator}{custom_slug}'
            try:
                slug = cls.objects.get(slug=slug_id)
            except cls.DoesNotExist:
                break
            else:
                # slug exists in db, check if expired to be modified:
                if slug.expired():
                    break
        return slug_id


class SlugClickCounter(models.Model):
    slug = models.OneToOneField(Url, on_delete=models.CASCADE, primary_key=True)
    click_counter = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.slug} : {self.click_counter}'


class FunnyQuoteManager(models.Manager):
    def random(self):
        """Draws `Funny Quote` from database."""
        len_db = self.aggregate(count=models.aggregates.Count('id'))['count']
        idx = random.randint(0, len_db-1)
        return self.all()[idx]


class FunnyQuote(models.Model):
    id = models.AutoField(primary_key=True)
    quote = models.CharField(max_length=128)

    objects = FunnyQuoteManager()

    def __str__(self):
        return f'{self.quote}'
