from rest_framework.permissions import BasePermission



class SlugUserPermission(BasePermission):
    message = 'You cannot access slug that is not created by you.'
    def has_object_permission(self, request, view, model_instance):
        return model_instance.user == request.user
