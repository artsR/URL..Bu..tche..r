from rest_framework import generics

from django.shortcuts import render

from .serializers import SlugSerializer
from urlbutcher.models import Url



class SlugList(generics.ListCreateAPIView):
    queryset = Url.objects.all()
    serializer_class = SlugSerializer
    pass
