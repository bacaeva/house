from rest_framework.permissions import BasePermission

#проверка на автора


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and\
               request.user == obj.user