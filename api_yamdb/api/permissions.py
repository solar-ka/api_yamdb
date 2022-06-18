from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorAdminModeratorOrReadOnly(BasePermission):
    """
    Позволяет редактировать и удалять объекты только
    их автору/администратору/модератору.
    """

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or request.user.role in ('admin', 'moderator')
        )


class ReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
