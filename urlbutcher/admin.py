from django.contrib import admin

from .models import FunnyQuote, Url



# Register your models here.

admin.site.register(Url)
admin.site.register(FunnyQuote)
