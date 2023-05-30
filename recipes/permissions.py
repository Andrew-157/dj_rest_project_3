from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_superuser


class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user


class IsParentObjectAuthorOrReadOnly(BasePermission):
    # This permission returns True for an object
    # only if the user is the creator of the parent of the object
    # For example: We have Recipe model that has author field as Foreign Key
    # and RecipeImage model for which Recipe is a parent, but it does not have
    # author field, so we check if the user is an author of parent Recipe
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.recipe.author == request.user
