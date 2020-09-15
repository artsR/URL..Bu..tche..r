import random
from datetime import datetime, timedelta

from django.db import models
from django.utils import timezone

# Create your models here.
EXPIRES_IN = 7


class Url(models.Model):
    slug = models.CharField(max_length=150, primary_key=True)
    url = models.URLField(max_length=512)
    created_at = models.DateTimeField(default=timezone.now, blank=True)

    def expired(self):
        return self.created_at + timedelta(days=EXPIRES_IN) < timezone.now()

    @classmethod
    def get_unique_slug(cls, alphabet, *, k=6, custom_slug='', sep=''):
        """Generates unique slug. Ready to save into database.

        Args:
            alphabet: Population of characters to draw
            k: Number of characters to draw
            custom_slug: Suffix slug eg. funny quote
            sep: Seperator between random prefix and custom suffix
        """
        #TODO: add some kind of timeout...
        while True:
            slug_id = ''.join(
                c for c in random.choices(alphabet, k=k) if c != ' '
            )
            slug_id = f'{slug_id}{sep}{custom_slug}'
            try:
                slug = cls.objects.get(slug=slug_id)
            except cls.DoesNotExist:
                break
            else:
                # slug exists in db, check if expired to be modified:
                if slug.expired():
                    break
        return slug_id

    def __str__(self):
        return f'{self.url}\n{self.slug}'


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
