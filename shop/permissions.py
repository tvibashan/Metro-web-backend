from rest_framework.permissions import BasePermission

class IsDriver(BasePermission):
    """
    Custom permission to only allow drivers to access the endpoint.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='driver').exists()
