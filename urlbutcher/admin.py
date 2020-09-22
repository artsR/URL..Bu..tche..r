from django.contrib import admin

from .models import FunnyQuote, Url



admin.site.register(Url)
admin.site.register(FunnyQuote)
