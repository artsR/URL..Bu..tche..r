from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse

from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils import timezone

from .permissions import SlugUserPermission, IsAdminUserOrReadOnly
from .serializers import SlugSerializer
from urlbutcher.models import Url



@api_view(['GET'])
def api_root(request):
    return Response({
        'slugs': reverse('api:slug_list', request=request),
    })


class SlugList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, SlugUserPermission]
    serializer_class = SlugSerializer

    def get_queryset(self):
        current_user = self.request.user
        return current_user.url_set.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SlugDetail(generics.RetrieveUpdateDestroyAPIView, SlugUserPermission):
    permission_classes = [IsAuthenticated, SlugUserPermission]
    queryset = Url.objects.all()
    serializer_class = SlugSerializer

    def partial_update(self, request, *args, **kwargs):
        """Prolongates expire data for slug."""
        instance = self.get_object()
        instance.created_at = timezone.now()
        # Save and Let to know signals to not reset click counter:
        instance.save(update_fields=['created_at'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
