from rest_framework import generics

from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.permissions import BasePermission

from .serializers import SlugSerializer
from urlbutcher.models import Url



class SlugUserPermission(BasePermission):
    message = 'You cannot access slug that is not created by you.'
    def has_object_permission(self, request, view, model_instance):
        return model_instance.user == request.user



class SlugList(generics.ListCreateAPIView):
    permission_classes = [SlugUserPermission]
    serializer_class = SlugSerializer

    def get_queryset(self):
        current_user = self.request.user
        return current_user.url_set.all()


class SlugDetail(generics.RetrieveDestroyAPIView, SlugUserPermission):
    permission_classes = [SlugUserPermission]
    queryset = Url.objects.all()
    serializer_class = SlugSerializer
