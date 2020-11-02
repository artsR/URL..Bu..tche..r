from rest_framework.permissions import BasePermission, IsAdminUser, SAFE_METHODS



class SlugUserPermission(BasePermission):
    message = 'You cannot access slug that is not created by you.'
    def has_object_permission(self, request, view, model_instance):
        return model_instance.user == request.user


class IsAdminUserOrReadOnly(IsAdminUser):
    def has_permission(self, request, view):
        is_admin = super(IsAdminUserOrReadOnly, self).has_permission(request, view)
        return is_admin or request.method in SAFE_METHODS
