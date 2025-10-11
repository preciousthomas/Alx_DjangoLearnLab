from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Allows only owners (authors) to edit or delete objects.
    Read-only is allowed for any request.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only to the author
        return getattr(obj, 'author', None) == request.user
    from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Allow only authors to edit or delete their own posts or comments.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user