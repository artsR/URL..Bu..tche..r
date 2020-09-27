from django.contrib import admin

from .models import FunnyQuote, Url, SlugClickCounter



admin.site.register(Url)
admin.site.register(FunnyQuote)
admin.site.register(SlugClickCounter)
