from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated

from .permissions import SlugUserPermission
from .serializers import SlugSerializer
from urlbutcher.models import Url



@api_view(['GET'])
def api_root(request):
    return Response({
        'slugs': reverse('api:slug_list', request=request),
    })


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
