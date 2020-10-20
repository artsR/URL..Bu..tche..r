from rest_framework import generics

from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated

from .permissions import SlugUserPermission
from .serializers import SlugSerializer
from urlbutcher.models import Url





class SlugList(generics.ListCreateAPIView):
    permission_classes = [SlugUserPermission, IsAuthenticated]
    serializer_class = SlugSerializer

    def get_queryset(self):
        current_user = self.request.user
        return current_user.url_set.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SlugDetail(generics.RetrieveDestroyAPIView, SlugUserPermission):
    permission_classes = [SlugUserPermission, IsAuthenticated]
    queryset = Url.objects.all()
    serializer_class = SlugSerializer
