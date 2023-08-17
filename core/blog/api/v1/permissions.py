from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission to only allowed owners of object to edit.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        # Instnce must have an attribute "user"
        return obj.author.user == request.user