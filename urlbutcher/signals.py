from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.http import request

from .models import Url, SlugClickCounter



FIELDS_PREVENT_RESET_COUNTER = {'created_at'}

@receiver(post_save, sender=Url)
def new_slug_click_counter(sender, instance, created, **kwargs):
    if created:
        if instance.user is not None:
            # slug created by authenticated user, so set counter to 0:
            SlugClickCounter.objects.update_or_create(
                slug=instance,
                defaults={'click_counter': 0}
            )

@receiver(post_save, sender=Url)
def update_slug_click_counter(sender, instance, created, **kwargs):
    if not created:
        update_fields = kwargs.get('update_fields', None)
        should_reset_counter = (
            True if update_fields is None
            else not update_fields.issubset(FIELDS_PREVENT_RESET_COUNTER)
        )
        if instance.user is None:
            # slug overwritten by anonymous user so delete existing counter:
            SlugClickCounter.objects.filter(slug=instance.slug).delete()
        elif should_reset_counter:
            SlugClickCounter.objects.update_or_create(
                slug=instance.slug,
                defaults={'click_counter': 0}
            )
