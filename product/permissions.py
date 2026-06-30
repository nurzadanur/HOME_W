from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_staff
            and (request.method in SAFE_METHODS or request.method in ['PUT', 'DELETE'])
        )
